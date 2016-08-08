import plac
import os, errno, subprocess
from reuseableCode import findInFile
from kripkeModelConstructor import kripkeModelConstructor

class driverObj(object):
    def __init__(self, mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, optionalConditionsFileName, startingNumWorlds):
        self.mainDir = mainDir
        self.theoryFileDir = theoryFileDir
        self.theoryFileName = theoryFileName
        self.instanceFileDir = instanceFileDir
        self.instanceFileName = instanceFileName
        self.EnfragmoOutputDir = EnfragmoOutputDir
        self.EnfragmoOutputFileName = EnfragmoOutputFileName
        self.optionalConditionsFileName = optionalConditionsFileName
        self.startingNumWorlds = startingNumWorlds
        self.findMaxNumWorlds()


    def findMaxNumWorlds(self):
        with open(self.instanceFileDir+self.instanceFileName, 'r') as f:
            numSubformulas = int(f.readline().split(']')[0][-1])

        self.maxWorlds = 2**numSubformulas  # theoretical upper bound for modal logics with FMP


    def runAndMinimizeModel(self):
        '''
        Figured I'd suck the calls to runEnfragmo and EnfragmoOutputToKripkeStructure
        out so that either a user can run them once with a specific instance file,
        or this drivingProc can be invoked multiple times
        '''
        isUnSAT = True
        currNumWorld = self.startingNumWorlds
        # loop around runEnfragmo call, changing the instanceFile each iteration; finds first power of 2 that yields a model
        while isUnSAT and currNumWorld <= self.maxWorlds:
            isUnSAT = self.makeModel(currNumWorld)
            if isUnSAT:
                currNumWorld *= 2

        if isUnSAT:
            print("\nThe formula failed to have a satisfying model with at most "+str(self.maxWorlds)+" worlds.\n")
        else:  # want to search on interval 2^{k-1} to 2^k, where k = currNumWorld
            self.halvingProc(int(currNumWorld/2), currNumWorld)


    def makeModel (self, currNumWorld):
        self.changeNumWorlds(currNumWorld)
        self.runEnfragmo()
        return self.EnfragmoOutputToKripkeStructure(currNumWorld)


    def halvingProc (self, lowerBound, upperBound):
        found = upperBound
        self.EnfragmoOutputFileName = self.EnfragmoOutputFileName.split('.')[0]+'-minimal.txt'

        # need to make sure lower bound is still on appropriate interval; we don't want to change it below!
        while lowerBound <= upperBound:
            # Must use integer division to get floor of midpoint because otherwise, due to proof, if floor was actual lower
            # bound, then ceiling will also yield satisfying model, but the ceiling wouldn't be the minimal model w.r.t. worlds!
            midpoint = int((upperBound + lowerBound) / 2)  # integer division for midpoint on interval
            UNSAT = self.makeModel(midpoint)
            if UNSAT:
                # if no model found at midpoint, lower bound must be in upper half of interval
                lowerBound = midpoint+1
            else:
                # We have found a model, so either midpoint is smallest num worlds, or it is upper bound and must look in lower interval
                upperBound = midpoint-1
                found = midpoint  # since midpoint succeeded

        #  Must run makeModel one more time on midpoint due to halting condition overwriting when approaching from above
        #  Rerun last model you found!
        self.makeModel(found)


    def changeNumWorlds(self, newNumWorlds):
        '''
            Given a user-specified instance file, creates a new Enfragmo problem
            instance file with the desired number of worlds. This procedure changes
            the original file supplied.
        '''
        instanceFileContents = [line.strip() for line in open(self.instanceFileDir+self.instanceFileName)]

        numWorldsLine = findInFile(instanceFileContents, lambda x: "TYPE World" in x)

        instanceFileContents[numWorldsLine] = 'TYPE World [1.. '+str(newNumWorlds)+']'
        outputFile = open(self.instanceFileDir+self.instanceFileName, 'w+')
        for line in instanceFileContents:
            outputFile.write("%s\n" % line.strip())


    def runEnfragmo(self):
        '''
            Runs Enfragmo given the theory file and instance file

            Need to change number of worlds required, given in the problem instance
            file, until 2*k fails but 2*(k+1) succeeds. Later, will implement binary
            search in this range. Future research will create Enfragmo instance
            file based on the model produced, and will send that off to Enfragmo again
            to further minimize the model.
        '''
        cmdList = [self.mainDir+'Enfragmo', self.theoryFileDir+self.theoryFileName, self.instanceFileDir+self.instanceFileName]
        output = subprocess.Popen(cmdList, stdout=subprocess.PIPE).stdout#.communicate()[0]

        if not os.path.exists(self.EnfragmoOutputDir):
            os.makedirs(self.EnfragmoOutputDir)
        outputFile = open(self.EnfragmoOutputDir+self.EnfragmoOutputFileName, 'w+')

        for line in output:
            outputFile.write(str(line).strip('b\'').strip('b\"').strip(r'\n') + '\n')


    def EnfragmoOutputToKripkeStructure(self, currNumWorld):
        '''
            Initially, this method will simply take the content from the runEnfragmo
            method, and will invoke the kripkeModelConstructor module on that output.
            Later, I will run Enfragmo again with a new specification file dictating
            the rules for how to
        '''
        ModelOutputDir = self.EnfragmoOutputDir+"Kripke Models/"
        if not os.path.exists(ModelOutputDir):
            os.makedirs(ModelOutputDir)
        KM= kripkeModelConstructor(self.instanceFileDir+self.instanceFileName, self.instanceFileName, self.EnfragmoOutputDir+self.EnfragmoOutputFileName, self.EnfragmoOutputFileName, ModelOutputDir)
        if KM.readEnfragmoOutput():
            KM.parseEnfragmoOutput()
            KM.parseInstanceFile()
            KM.printKripkeModel()
            return False  # A satisfying model has been found for the formula, therefore the loop can be halted
        else:
            return True  # The formula fails to have a model with this number of worlds


def insertRelationConditions(theoryFileDir, theoryFileName, optionalConditionsFileName):
    '''
        Given a user-specified file, creates a new Enfragmo theory file which
        includes those new conditions on the relation; these may or may not
        necessarily correspond with normal axiom characterizations. This
        procedure generates a new theory file, rather than wiping out the old
        one.
    '''

    newTheoryFileContents = [line.strip() for line in open(theoryFileDir+theoryFileName)]

    a = findInFile(newTheoryFileContents, lambda x: "PRINT :" in x)
    printRelationLines = newTheoryFileContents[a:]
    newTheoryFileContents = newTheoryFileContents[:a]
    newTheoryFileContents.extend([line.strip() for line in open(theoryFileDir+optionalConditionsFileName)])
    newTheoryFileContents.extend(printRelationLines)

    newTheoryFileName = theoryFileName.split('.')[0]+'-AdditionalConditions.T'

    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

    try:
        file_handle = os.open(theoryFileDir+newTheoryFileName,flags)
    except OSError as e:
        if e.errno == errno.EEXIST:  # Failed as the file already exists.
            pass
        else:  # Something unexpected went wrong so reraise the exception.
            raise
    else:  # No exception, so the file must have been created successfully.
        with os.fdopen(file_handle, 'w') as outputFile:
            for line in newTheoryFileContents:
                outputFile.write("%s\n" % line.strip())

    return newTheoryFileName


def main(mainDir='/home/wbkboyer/GitHub/MSS-SupplementaryFiles/', theoryFileDir='Single Modality/', theoryFileName='MLDecisionProcK.T', instanceFileDir='', instanceFileName='', optionalConditionsFileName='', startingNumWorlds=1):
    "Run Enfragmo with desired Theory file and problem instance file, optionally with additional conditions."

    ''' For the required theory and problem instance files, please clone the repository:
            https://github.com/wandaboyer/MSS-SupplementaryFiles.git

    Directory structure should be as follows:
        <Main Directory>
            Enfragmo
            Theory files/
                Single Modality/
                    <optional conditions>.txt
                    MLDecisionProcK.T
            Instance Files/
                <problem instance>.I
            Output/
                <output>.txt
                Kripke Models/
                    <model picture>.svg

    This is subject to change as I reorganize my project.
    '''
    EnfragmoOutputDir = mainDir + r"Output/"+instanceFileDir
    theoryFileDir=mainDir+'Theory Files/'+theoryFileDir
    instanceFileDir=mainDir+'Instance Files/'+instanceFileDir

    if optionalConditionsFileName is not '':
        theoryFileName = insertRelationConditions(theoryFileDir, theoryFileName, optionalConditionsFileName)

    #  "document sequencer"
    if instanceFileName is not '': #only one instance file specified to run procedure on
        EnfragmoOutputFileName = instanceFileName.split('.')[0]+'Out.txt'
        driverForFormula = driverObj(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, optionalConditionsFileName, startingNumWorlds)
        driverForFormula.runAndMinimizeModel()
    else:  # run procedure on entire instance file directory
        for instanceFileDir, subdirList, fileList in os.walk(instanceFileDir, topdown=False):
            for instanceFileName in fileList:
                if instanceFileName.endswith('.I'):
                    print("\n\n Processing "+instanceFileName+"\n_______\n")
                    EnfragmoOutputFileName = instanceFileName.split('.')[0]+'Out.txt'
                    driverForFormula = driverObj(mainDir, theoryFileDir, theoryFileName, instanceFileDir+'/', instanceFileName, EnfragmoOutputDir+instanceFileDir.split('/')[-1]+'/', EnfragmoOutputFileName, optionalConditionsFileName, startingNumWorlds)
                    driverForFormula.runAndMinimizeModel()

if __name__ == '__main__':
    plac.call(main)