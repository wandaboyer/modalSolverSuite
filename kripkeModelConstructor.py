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
        From the Enfragmo output, find the tuples dictating the accessibility 
        relation. The result will appear as follows:
            R = {(j,k), ..., (l,m)} with worlds j,k,l,m in W.
        
        In the future, with multiple modalities, need to be able to use first
        argument of tuple to separate different agents from the others. 
            That is, for each agent i: R_i = {(j,k),...(l,m)} will express their
            accessibility relation with worlds j,k,l,m in W.
        '''
    def readValuation(self):
        '''
        The valuation map is dictated by the TrueAt predicate, and will appear:
        
            <PredicateSymbol><BasicInfo Name='TrueAt'....
                <DataSet Name= 'TrueAt' TypeSize= '2' >
                    <ARow><IntValue Name= '1'/><IntValue Name= '1'/><True/></ARow>
                    ...
                </DataSet>
            </PredicateInfo>
            
        The human-readable output will appear as:
            V(w) = {p_i, ... p_j} for each world w in W and propositional atoms
            p_i.
        '''
         
    def printKripkeModel(self):
        '''
        Take each of the components and print them out
        '''
        outputFile = open(self.ModelOutputDir+self.InstanceFilename+'-kripkeModel.txt', 'w+')
        
        for component in self.kripkeStructure:
            outputFile.write("%s\n" % component.strip()) 

            
class KripkeStructure(object):
    '''
    The Kripke structure will be an instance of the KripkeStructure class, which
    will have the following components:
    
    '''
    def __init__(self):
        '''
        '''
    
 
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
        #thing.printKripkeModel()
    else:
        print("The formula described in instance file "+instanceFilename+".I was determined to be unsatisfiable by Enfragmo, and therefore doesn't have a satisfying Kripke structure.")