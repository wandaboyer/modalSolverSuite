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

    def __init__(self, InstanceFilepath, InstanceFilename, EnfragmoOutputFilepath, EnfragmoOutputFilename, ModelOutputDir):
        '''
        Receives the name of the modal benchmark formula file to be converted.
        '''
        self.InstanceFilepath = InstanceFilepath
        self.InstanceFilename = InstanceFilename
        self.EnfragmoOutputFilepath = EnfragmoOutputFilepath
        self.EnfragmoOutputFilename = EnfragmoOutputFilename
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
            R = {j: [k,l], ..., m: [n,o]} with worlds j, k, l, m, n, o in W.
        
        In the future, with multiple modalities, need to be able to use first
        argument of tuple to separate different agents from the others. 
            That is, for each agent i: R_i = {(j,k),...(l,m)} will express their
            accessibility relation with worlds j,k,l,m in W.
        '''
        return extractTuples(self.EnfragmoOutputFileLines,"TrueAt")
        
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
        Implemented through the use of a dictionary (world will be the key, and
        a list of propositional atoms true at that world will be the value).
        '''
        dictionary = extractTuples(self.EnfragmoOutputFileLines, "Accessible")
        print(dictionary)
        return dictionary
    
    
    def parseInstanceFile(self):
        verifierObject = verifier(self.InstanceFilepath)
        verifierObject.readProblemInstanceFile()
        verifierObject.parseProblemInstanceFile()
        self.numWorlds = verifierObject.numWorlds()
        
        #print(str(self.numDistinctAtoms) + " " + str(self.numWorlds))
        self.KM.setW([str(i) for i in range(1, self.numWorlds+1)])
        #self.KM.setPropAtoms([verifierObject.SameAtomList.get_leader(equivClass) for equivClass in verifierObject.SameAtomList])
        #print(self.atomicSubformulas)
    
         
    def printKripkeModel(self):
        '''
        Take each of the components and print them out
        '''
        outputFile = open(self.ModelOutputDir+self.InstanceFilename+'-kripkeModel.txt', 'w+')
        self.KM.displayKripkeStructure(outputFile)
        #for component in self.kripkeStructure:
        #    outputFile.write("%s\n" % component.strip()) 
        
           
class KripkeStructure(object):
    '''
    The Kripke structure will be an instance of the KripkeStructure class, which
    will have the following components:
    
    '''
    def __init__(self):
        self.graph = gv.Digraph(format='svg')
        
    def setValuation(self, valuationDict):
        self.__valuationMap = valuationDict
        #print(self.__valuationMap)
      
    def setW(self, worldList):
        '''
        Take the dict of the valuation map to label each world
        '''
        self.__worldList = worldList
        for world in self.__worldList:
            self.graph.node(world, {'label': str(self.__valuationMap.get(world))})
 
    def setAccessible(self,accessibilityDict):
        self.__accessibilityRelation = accessibilityDict
        for key, relatesTo in accessibilityDict.iteritems():
            for world in relatesTo:
                self.graph.edge(key,world)
    
    def displayKripkeStructure(self, outputFile):
        print(self.graph.source)
        self.graph.render(outputFile)
            
'''
Testing
'''     
if __name__ == "__main__":
    instanceFileDir = "/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/"
    #instanceFilename = "needsNonReflexiveModel"
    instanceFilename = "multipleSameAtoms"
    
    EnfragmoOutputDir = "/home/wanda/Documents/Dropbox/Research/Final Project/Output/"
    #EnfragmoOutputFilename = "needsNonReflexiveModelOut"
    EnfragmoOutputFilename = instanceFilename+"Out"
    
    ModelOutputDir = EnfragmoOutputDir+"Kripke Models/"
    
    thing = kripkeModelConstructor(instanceFileDir+instanceFilename+'.I', instanceFilename, EnfragmoOutputDir+EnfragmoOutputFilename+'.txt', EnfragmoOutputFilename, ModelOutputDir)
    
    if thing.readEnfragmoOutput():
        thing.parseEnfragmoOutput()
        thing.parseInstanceFile()
        thing.printKripkeModel()
    else:
        print("The formula described in instance file "+instanceFilename+".I was determined to be unsatisfiable by Enfragmo, and therefore doesn't have a satisfying Kripke structure.")