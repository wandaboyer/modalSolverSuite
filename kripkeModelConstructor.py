'''
Created on Jun 13, 2015

@author: wandaboyer
'''
import graphviz as gv
from verifier import verifier

from reuseableCode import findInFile
from modalSolverSuite.reuseableCode import extractTuples

class kripkeModelConstructor(object):
    '''
    This program takes the output from the Enfragmo system and produces the 
    Kripke model found, if one exists, or indicates that the formula is UNSAT.
    '''

    def __init__(self, InstanceFilepath, InstanceFilename, EnfragmoOutputFilepath, EnfragmoOutputFileName, ModelOutputDir):
        '''
        Receives the name of the modal benchmark formula file to be converted.
        '''
        self.InstanceFilepath = InstanceFilepath
        self.InstanceFilename = InstanceFilename
        self.EnfragmoOutputFilepath = EnfragmoOutputFilepath
        self.EnfragmoOutputFilename = EnfragmoOutputFileName
        self.ModelOutputDir = ModelOutputDir
        
        self.KM = KripkeStructure()
    
    def readEnfragmoOutput(self):
        '''
        Opens file and reads into a list
        '''
        self.EnfragmoOutputFileLines = [line.strip() for line in open(self.EnfragmoOutputFilepath) if line != '\n']
        
        if "<Satisfiable/>" in self.EnfragmoOutputFileLines[4]:
            return True
    
    def parseEnfragmoOutput(self):
        self.KM.setValuation(self.readValuation())
        self.KM.setAccessible(self.readAccessible())
        
    def readAccessible(self):
        '''
        From the Enfragmo output, find the tuples dictating the accessibility 
        relation. The result will be stored in a dictionary, with the first
        member of the tuple appearing as the key, and the worlds it relates to
        will appear in a list as the value:
            R = {j: (k,l), ..., m: (n,o)} with worlds j, k, l, m, n, o in W.
        
        In the future, with multiple modalities, need to be able to use first
        argument of tuple to separate different agents from the others. 
            That is, for each agent i: R_i = {(j,k),...(l,m)} will express their
            accessibility relation with worlds j,k,l,m in W.
        '''
        return extractTuples(self.EnfragmoOutputFileLines,"Accessible")
        
    def readValuation(self):
        '''
        The valuation map is dictated by the TrueAt predicate, and will appear:
        
            <PredicateSymbol><BasicInfo Name='TrueAt'....
                <DataSet Name= 'TrueAt' TypeSize= '2' >
                    <ARow><IntValue Name= '1'/><IntValue Name= '1'/><True/></ARow>
                    ...
                </DataSet>
            </PredicateInfo>
            
        The data will be stored in a defaultdict, where the subformula will be the key,
        and a list of worlds that subformula is true at will be the value:
            R = {s_1: (k,l), ..., s_k: (n,o)} for each subformula s_i and propositional
            atoms k,l,n,o,...
        '''
        return extractTuples(self.EnfragmoOutputFileLines, "TrueAt") # key is world, entry is list of subformulas true at that world
    
    def parseInstanceFile(self):
        verifierObject = verifier(self.InstanceFilepath)
        verifierObject.readProblemInstanceFile()
        verifierObject.parseProblemInstanceFile()
        self.numWorlds = verifierObject.numWorlds()
        self.KM.setW(verifierObject.SameAtomList,[str(i) for i in range(1, self.numWorlds+1)])
        
    def printKripkeModel(self):
        '''
        Take each of the components and print them out
        '''
        outputFile = self.ModelOutputDir+self.InstanceFilename+'-kripkeModel'
        self.KM.displayKripkeStructure(outputFile)
        
           
class KripkeStructure(object):
    '''
    The Kripke structure will be an instance of the KripkeStructure class, which
    will have the following components:
    
    '''
    def __init__(self):
        self.graph = gv.Digraph(format='svg')
        
    def setValuation(self, valuationDict):
        self.__valuationMap = valuationDict
      
    def setW(self, atoms, worldList):
        for world in worldList:
            valuationLabel = set() # each world has a set of proposition letters true at that world
            for subformula in self.__valuationMap.get(world): # key is world, so from that list of subformulas
                if subformula in [key for key in atoms.leader]: # if the subformula corresponds with an atom
                    valuationLabel.add(atoms.get_leader(subformula)) # add that atom to the set of propositions true at the world
            valuationLabel = ', '.join(valuationLabel) # reassign valuationLabel to be a string which is concatenation of elements of the former set, namely a string of all atoms true at a world
            self.graph.node(str(world), label=valuationLabel,xlabel='w'+str(world)) #xlabel gives us the world label, label gives us the atoms true at the world.
 
    def setAccessible(self,accessibilityDict):
        for key, relatesTo in accessibilityDict.items():
            for world in relatesTo:
                self.graph.edge(str(key),str(world))
    
    def displayKripkeStructure(self, outputFile):
        print(self.graph.source) # doesn't render the string of atoms correctly, but does so in the resulting picture.
        self.graph.render(filename=outputFile)
            
'''
Testing
'''     
if __name__ == "__main__":
    instanceFileDir = r"/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/"
    #instanceFileName = "needsNonReflexiveModel"
    #instanceFileName = "multipleSameAtoms"
    instanceFileName = "falsumTester"
    
    EnfragmoOutputDir = r"/home/wanda/Documents/Dropbox/Research/Final Project/Output/"
    EnfragmoOutputFileName = instanceFileName+"Out"
    
    ModelOutputDir = EnfragmoOutputDir+"Kripke Models/"
    
    thing = kripkeModelConstructor(instanceFileDir+instanceFileName+'.I', instanceFileName, EnfragmoOutputDir+EnfragmoOutputFileName+'.txt', EnfragmoOutputFileName, ModelOutputDir)
    
    if thing.readEnfragmoOutput():
        thing.parseEnfragmoOutput()
        thing.parseInstanceFile()
        thing.printKripkeModel()
    else:
        print("The formula described in instance file "+instanceFileName+".I was determined to be unsatisfiable by Enfragmo, and therefore doesn't have a satisfying Kripke structure.")