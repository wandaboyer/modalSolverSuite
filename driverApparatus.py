'''
Created on Sep 14, 2015

@author: Wanda B. Boyer
@contact: wbkboyer@gmail.com
'''

import plac
import os, errno, subprocess
from reuseableCode import findInFile
from kripkeModelConstructor import kripkeModelConstructor


def insertRelationConditions(theoryFileDir, theoryFileName, optionalConditionsFileName):
    '''
        Given a user-specified file, creates a new Enfragmo theory file which
        includes those new conditions on the relation; these may or may not
        necessarily correspond with normal axiom characterizations. This 
        procedure generates a new theory file, rather than wiping out the old
        one.
    '''
    newTheoryFileContents = [line.strip() for line in open(theoryFileDir+theoryFileName)] #if line != '\n']
    
    a = findInFile(newTheoryFileContents, lambda x: "PRINT :" in x)
    printRelationLines = newTheoryFileContents[a:]
    newTheoryFileContents = newTheoryFileContents[:a]
    newTheoryFileContents.extend([line.strip() for line in open(theoryFileDir+optionalConditionsFileName)]) # if line != '\n'])
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


def changeNumWorlds(instanceFileDir, instanceFileName, newNumWorlds):
    '''
        Given a user-specified instance file, creates a new Enfragmo problem
        instance file with the desired number of worlds. This procedure changes
        the original file supplied.
    '''
    instanceFileContents = [line.strip() for line in open(instanceFileDir+instanceFileName)] #if line != '\n']
    
    numWorldsLine = findInFile(instanceFileContents, lambda x: "TYPE World" in x)
   
    instanceFileContents[numWorldsLine] = 'TYPE World [1.. '+str(newNumWorlds)+']'
    outputFile = open(instanceFileDir+instanceFileName, 'w+')
    for line in instanceFileContents:
        outputFile.write("%s\n" % line.strip())

    
def runEnfragmo(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName):
    '''
        Runs Enfragmo given the theory file and instance file
        
        Need to change number of worlds required, given in the problem instance
        file, until 2*k fails but 2*(k+1) succeeds. Later, will implement binary
        search in this range. Future research will create Enfragmo instance
        file based on the model produced, and will send that off to Enfragmo again
        to further minimize the model.
    '''
    cmdList = [mainDir+'Enfragmo', theoryFileDir+theoryFileName, instanceFileDir+instanceFileName]
    output = subprocess.Popen(cmdList, stdout=subprocess.PIPE).stdout#.communicate()[0]
    
    if not os.path.exists(EnfragmoOutputDir):
        os.makedirs(EnfragmoOutputDir)
    outputFile = open(EnfragmoOutputDir+EnfragmoOutputFileName, 'w+')
    
    for line in output:
        outputFile.write(str(line).strip('b\'').strip('b\"').strip(r'\n') + '\n')
    
    
def EnfragmoOutputToKripkeStructure(instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, currNumWorld):
    '''
        Initially, this method will simply take the content from the runEnfragmo
        method, and will invoke the kripkeModelConstructor module on that output.
        Later, I will run Enfragmo again with a new specification file dictating
        the rules for how to 
    '''
    ModelOutputDir = EnfragmoOutputDir+"Kripke Models/"
    KM= kripkeModelConstructor(instanceFileDir+instanceFileName, instanceFileName, EnfragmoOutputDir+EnfragmoOutputFileName, EnfragmoOutputFileName, ModelOutputDir)
    if KM.readEnfragmoOutput():
        KM.parseEnfragmoOutput()
        KM.parseInstanceFile()
        KM.printKripkeModel()
        #print("The formula has a model with "+str(currNumWorld)+" worlds.")
        return False  # A satisfying model has been found for the formula, therefore the loop can be halted
    else:
        #print("The formula described in instance file "+instanceFileName+" was determined to be unsatisfiable by Enfragmo, and therefore doesn't have a satisfying Kripke structure with "+ str(currNumWorld)+" worlds.")
        return True  # The formula fails to have a model with this number of worlds


def makeModel (mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, currNumWorld):
    changeNumWorlds(instanceFileDir, instanceFileName, currNumWorld)
    runEnfragmo(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName)
    return EnfragmoOutputToKripkeStructure(instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, currNumWorld)


def halvingProc (mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, minWorlds, maxWorlds):
    lowerBound = maxWorlds # this denotes our lower bound, which we will incrementally shrink
    minimalEnfragmoOutputFileName = EnfragmoOutputFileName.split('.')[0]+'-minimal.txt'

    # need to make sure lower bound is still on appropriate interval; we don't want to change it below!
    while minWorlds <= lowerBound:
        # Must use integer division to get floor of midpoint because otherwise, due to proof, if floor was actual lower
        # bound, then ceiling will also yield satisfying model, but the ceiling wouldn't be the minimal model w.r.t. worlds!
        midpoint = int((lowerBound + minWorlds) / 2) # integer division for midpoint on interval
        if makeModel(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, minimalEnfragmoOutputFileName, midpoint):
            # we have found a model, so either midpoint is smallest num worlds, or it is upper bound and must look in lower interval
            minWorlds = midpoint   # isUNSAT is TRUE so then the minimal model must be ABOVE the midpoint
        else:  # if no model found at midpoint, lower bound must be in upper half of interval
            lowerBound = midpoint


def runAndMinimizeModel(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, startingNumWorlds, maxWorlds):
    '''
    Figured I'd suck the calls to runEnfragmo and EnfragmoOutputToKripkeStructure
    out so that either a user can run them once with a specific instance file, 
    or this drivingProc can be invoked multiple times
    '''
    isUnSAT = True
    currNumWorld = startingNumWorlds
    # loop around runEnfragmo call, changing the instanceFile each iteration; finds first power of 2 that yields a model
    while isUnSAT and currNumWorld <= maxWorlds:
        isUnSAT = makeModel(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, currNumWorld)
        currNumWorld *= 2

    if isUnSAT:
        print("\nThe formula failed to have a satisfying model with at most "+str(maxWorlds)+" worlds.\n")
    else: # want to search on interval 2^{k-1} to 2^k, where k = currNumWorld
        halvingProc(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, currNumWorld/2, currNumWorld)


def drivingProc(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, optionalConditionsFileName, startingNumWorlds, maxWorlds):
    if optionalConditionsFileName is not '': # meaning there's a set of desired conditions for the AR sent by the user
        runAndMinimizeModel(mainDir, theoryFileDir, insertRelationConditions(theoryFileDir, theoryFileName, optionalConditionsFileName), instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, startingNumWorlds, maxWorlds)
    else: # no conditions on AR; guaranteed to find a finite model, because we are operating in modal logic K
        runAndMinimizeModel(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, startingNumWorlds, maxWorlds)


def findMaxNumWorlds(instanceFileDir, instanceFileName):
    with open(instanceFileDir+instanceFileName, 'r') as f:
        numSubformulas = int(f.readline().split(']')[0][-1])
    return 2**numSubformulas # theoretical upper bound for modal logic K


def main(mainDir='/home/wanda/Documents/Dropbox/Research/Final Project/', theoryFileName='MLDecisionProcK.T', instanceFileName='needsNonReflexiveModel.I', optionalConditionsFileName='', startingNumWorlds=1, maxWorlds='16'):
    "Run Enfragmo with desired Theory file and problem instance file, optionally with additional conditions."
    
    '''
    Directory structure should be as follows:
        <Main Directory>
            Enfragmo
            Theory files/
                <optional conditions>.txt
                Single Modality/
                    MLDecisionProcK<Characterization>.T
            Instance Files/
                <problem instance>.I
            Output/
                <output>.txt
                Kripke Models/
                    <model picture>.svg
                    
    This is subject to change as I re-organize my project.
    '''
    theoryFileDir=mainDir+r'Theory files/Single Modality/'
    instanceFileDir=mainDir+r'Instance Files/OtherTests/'
    
    EnfragmoOutputDir = mainDir+r"Output/Blargh/"
    #  "document sequencer"
    if instanceFileName is not 'RunAll': #only one instance file specified to run procedure on
        EnfragmoOutputFileName = instanceFileName.split('.')[0]+'Out.txt'
        # theoretical max num worlds... NEED TO KNOW IF THIS IS ACTUALLY IT FOR ALL POSSIBLE FC?!
        maxWorlds = findMaxNumWorlds(instanceFileDir, instanceFileName) # theoretical upper bound for modal logic K
        drivingProc(mainDir, theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName, optionalConditionsFileName, startingNumWorlds, maxWorlds)
    else: # run procedure on entire instance file directory
        for instanceFileDir, subdirList, fileList in os.walk(instanceFileDir, topdown=False):
            for instanceFileName in fileList:
                if instanceFileName.endswith('.I'):
                    print("\n\n"+instanceFileName+"\n_______\n")
                    EnfragmoOutputFileName = instanceFileName.split('.')[0]+'Out.txt'
                    maxWorlds = findMaxNumWorlds(instanceFileDir, instanceFileName)
                    drivingProc(mainDir, theoryFileDir, theoryFileName, instanceFileDir+'/', instanceFileName, EnfragmoOutputDir+instanceFileDir.split('/')[-1]+'/', EnfragmoOutputFileName, optionalConditionsFileName, startingNumWorlds, maxWorlds)     


if __name__ == '__main__':  
    plac.call(main)