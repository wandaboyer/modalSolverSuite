'''
Created on Jun 13, 2015

@author: wandaboyer
'''

from verifier import verifier

class kripkeModelConstructor(object):
    '''
    This program takes the output from the Enfragmo system and produces the 
    Kripke model found, if one exists, or indicates that the formula is UNSAT.
    '''

    def __init__(self, InstanceFilepath, InstanceFilename, EnfragmoOutputFilepath, EnfragmoOutputFilename, ModelOutputDir):
        '''
        Receives the name of the modal benchmark formula file to be converted.
        '''
        self.InstanceFilepath = InstanceFilepath
        self.InstanceFilename = InstanceFilename
        self.EnfragmoOutputFilepath = EnfragmoOutputFilepath
        self.EnfragmoOutputFilename = EnfragmoOutputFilename
        self.ModelOutputDir = ModelOutputDir
    
    def readEnfragmoOutput(self):
        '''
        Opens file and reads into a list
        '''
        self.EnfragmoOutputFileLines = [line.strip() for line in open(self.EnfragmoOutputFilepath) if line != '\n']
        
        if "<Satisfiable/>" in self.EnfragmoOutputFileLines[4]:
            return True
    
    def parseInstanceFile(self):
        verifierObject = verifier(self.InstanceFilepath)
        verifierObject.readProblemInstanceFile()
        self.numDistinctAtoms = verifierObject.countNumAtoms()
        self.numWorlds = verifierObject.numWorlds()
        
        #print(str(self.numDistinctAtoms) + " " + str(self.numWorlds))
        self.worldSet = [str(i) for i in range(1, self.numWorlds+1)]
        self.atomSet = ["p"+str(i) for i in range(1, self.numDistinctAtoms+1)]
        self.atomicSubformulas = verifierObject.SameAtomList
        print(self.atomicSubformulas)
    
    def parseEnfragmoOutput(self):
        self.readAccessible()
        self.readValuation()
    
    def readAccessible(self):
        '''
        '''
    def readValuation(self):
        '''
        '''
         
    def printKripkeModel(self):
        '''
        Sends result to a file.
        '''
        outputFile = open(self.ModelOutputDir+self.InstanceFilename+'-kripkeModel.txt', 'w+')
        
        for component in self.kripkeStructure:
            outputFile.write("%s\n" % component.strip())  
'''
Testing
'''     
if __name__ == "__main__":
    instanceFileDir = "/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/"
    instanceFilename = "needsNonReflexiveModel"
    
    EnfragmoOutputDir = "/home/wanda/Documents/Dropbox/Research/Final Project/Output/"
    EnfragmoOutputFilename = "needsNonReflexiveModelOut"
    
    ModelOutputDir = EnfragmoOutputDir+"Kripke Models/"
    
    thing = kripkeModelConstructor(instanceFileDir+instanceFilename+'.I', instanceFilename, EnfragmoOutputDir+EnfragmoOutputFilename+'.xml', EnfragmoOutputFilename, ModelOutputDir)
    
    if thing.readEnfragmoOutput():
        thing.parseEnfragmoOutput()
        thing.parseInstanceFile()
        thing.printKripkeModel()
    else:
        print("The formula described in instance file "+instanceFilename+".I was determined to be unsatisfiable by Enfragmo, and therefore doesn't have a satisfying Kripke structure.")