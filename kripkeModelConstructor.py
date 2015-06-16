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
    
    def parseEnfragmoOutput(self):
        '''
        Determines whether the formula is unsatisfiable; if so, the procedure
        halts. If not, then the necessary information is extracted from both the
        problem instance file and the output from Enfragmo.
        '''
        
        return True
    
    def parseInstanceFile(self):
        verifierObject = verifier(self.InstanceFilepath)
        verifierObject.readProblemInstanceFile()
        self.numDistinctAtoms = verifierObject.countNumAtoms()
        self.numWorlds = verifierObject.numWorlds()
         
    def printKripkeModel(self):
        '''
        Sends result to a file.
        '''  
        #print(str(self.numDistinctAtoms) + " " + str(self.numWorlds))  
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