'''
Created on Jan. 12, 2015

@author: Wanda B. Boyer
@contact: wbkboyer@gmail.com
'''
from treelib import Tree, Node

import re
from union_find import unionfind
 
from reuseableCode import findInFile
 
class verifier(object):
    '''
    This verifier object is intended to receive an Enfragmo instance file,
    and then to determine the original formula corresponding to that file.
    Each subformula which is an atom will be given as a lower-case letter,
    and nesting of formulas will be indicated by appropriate bracketing.
    The symbols used to represent operators are as follows:
        And           &
        Or            v
        Not           ~
        Implication   ->
        Box           box
        Diamond       dia
    With unary operators applied directly to atoms being dropped.
    
    The format of an instance file is assumed to be as follows:
    
        TYPE  Subformula [ 1.. n]
        TYPE World [1..m]
        PREDICATE Atom
        
        ...
        
        PREDICATE And
        ...
        
        PREDICATE Or
        ...
        
        PREDICATE Not
        ...
        
        PREDICATE Implication
        ...
        
        PREDICATE Box
        ...
        
        PREDICATE Diamond
        ...
        
        PREDICATE SameAtom
        
    Where "..." indicates that either singletons, pairs, or triples will occupy
    the lines below the current PREDICATE delimiter and the next, signifying
    the appropriate relationship between the subformulas. For example,
    
        PREDICATE And
        (1, 2, 3)
        
    Indicates that the main connective of subformula 1 is conjunction, and that
    subformula 2 and 3 are the two operands for that operator.
    '''
    
    def __init__(self, filename):
        '''
        Receives the name of the instance file to be verified, then uses this
        to initialize the corresponding tree structure 
        '''
        self.SameAtomList = unionfind.UnionFind()

        self.filename = filename      
        
    def readProblemInstanceFile(self):
        '''
        This method assumes that the instance file exists and is correctly
        formatted.
        
        Subformulas are labeled in pre-order DFS traversal fashion, so as to
        allow the numbering to reflect the operator/operand relationship.
        '''
        self.instanceFileLines = [line.strip() for line in open(self.filename) if line != '\n']
    
    def parseProblemInstanceFile(self):
        self.countNumTreeNodes()
        self.countNumTreeLeaves()
        self.countNumAtoms()
        self.setUpSameAtomList()
        self.buildTree()
     
    def numWorlds(self):
        return int(self.instanceFileLines[1][-2])
        
    def countNumTreeNodes(self):
        '''
        The number of tree nodes is inherent in the number of subformulas,
        which is given on the first line of a well-formed problem instance
        file. In this way, the given formula is considered to be the first
        subformula, where its main connective labels the root node, and its
        '''
        self.numTreeNodes = int(self.instanceFileLines[0].split(" ")[-1].split("]")[0])
        
    def countNumTreeLeaves(self):
        '''
        The number of tree leaves is simply the number of singletons that 
        satisfy Atom, including duplicates.
        '''
        self.numTreeLeaves = \
            int((self.instanceFileLines.index("PREDICATE SameAtom") - 1)- \
             self.instanceFileLines.index("PREDICATE Atom"))
    
    def countNumAtoms(self):
        '''
        Since multiple subformulas can refer to the same atom, need to subtract
        the count of pairs satisfying SameAtom from the total count of
        subformulas satisfying Atom. This can be done by counting the number of
        entries between each of the appropriate PREDICATE identifiers (given a 
        well-formed instance file).
        '''
        self.numAtoms = int((self.instanceFileLines.index("PREDICATE And")- \
                            (self.instanceFileLines.index("PREDICATE Atom")+1) - \
                           (len(self.instanceFileLines) - \
                           (self.instanceFileLines.index("PREDICATE SameAtom")+1))))
        return self.numAtoms        
      
    def assignSymbol(self, label):
        if label == "And":
            return "&"
        elif label == "Or":
            return "v"
        elif label == "Not":
            return "~"
        elif label == "Implication":
            return "->"
        elif label == "Biconditional":
            return "<->"
        elif label == "Box":
            return "box"
        elif label == "Diamond":
            return "dia"
    
    def assignAtom(self, i):
        
        '''for atomEquivClass in self.SameAtomList.get_sets(): # each equivalence class is labeled by index
            if str(i) in atomEquivClass: # if any equivalence class contains the subformula, 
                #print(atomEquivClass)
                return self.SameAtomList.get_leader(str(i)) # then assign the representative atom label
            else:
                print(i)
                #print(self.SameAtomList)
                self.SameAtomList.insert(str(i))
                print(atomEquivClass)
                #print(self.SameAtomList)
            #j = j+1'''
        for atomEquivClass in self.SameAtomList.get_sets():
            if str(i) in atomEquivClass: # if any equivalence class contains the subformula, 
                return self.SameAtomList.get_leader(str(i)) # then assign the representative atom label
            
        self.SameAtomList.insert(str(i))
        return self.SameAtomList.get_leader(str(i))
        #for set in self.SameAtomList.get_sets():
            
    def setUpSameAtomList(self):
        '''
        Using the Union Find datastructure, I will keep track of the equivalence
        classes of SameAtoms and then supply a label based on the index of the
        subset in which a subformula corresponding with an atom is contained.
        '''
        
        startIndexSameAtoms = findInFile(self.instanceFileLines, lambda x: "PREDICATE SameAtom" in x) + 1
        sameAtomPairs = self.instanceFileLines[startIndexSameAtoms:]
        
        for pair in sameAtomPairs:
            tmp = pair.split(",")
            label1 = tmp[0].split("(")[1]
            label2 = tmp[1].split(")")[0]
            self.SameAtomList.insert(label1, label2)     
        #print(self.SameAtomList)
    def determineConnective(self, i):
        '''
        Each subformula label is guaranteed to be the first argument of some
        tuple; either it will correspond with an atom, the only argument,
        or it will correspond with the main connective of a unary 
        (i.e. negation, box, or diamond) or binary (i.e. conjunction or 
        disjunction) subformula.
        '''
        SiThing=findInFile(self.instanceFileLines, lambda x: "("+str(i)+")" in x)
        if SiThing:
            for k in range(SiThing, 0, -1): # go back in the file until you can find out what predicate we're dealing with
                if self.instanceFileLines[k].split(" ")[0] == "PREDICATE":
                    if self.instanceFileLines[k].split(" ")[1] == "Falsum":
                        return "false"
            return self.assignAtom(i)
        if findInFile(self.instanceFileLines, lambda x: "("+str(i)+"," in x):
            SiAsMainConnective = findInFile(self.instanceFileLines, lambda x: "("+str(i)+"," in x)
            for j in range(SiAsMainConnective, 0, -1): # go back in the file until you can find out what predicate we're dealing with
                if self.instanceFileLines[j].split(" ")[0] == "PREDICATE":
                    if self.instanceFileLines[j].split(" ")[1] == "SameAtom": # if there are no tuples under SameAtom, then this isn't reached due to SiAsMainConnective
                        return self.assignAtom(i)
                    else:
                        return self.assignSymbol(self.instanceFileLines[j].split(" ")[1]) # if the predicate refers to an operator, then we need to find out which one!
    
    def nodeCreation(self, predicate, SiConnective, i):        
        SiAsOperand = findInFile(self.instanceFileLines, predicate)
        ParentOfSi = str(self.instanceFileLines[SiAsOperand].split(",")[0].split("(")[1])
        self.syntaxTree.create_node(SiConnective, str(i), parent=ParentOfSi)        
        
    def makeSyntaxTreeNode(self, SiConnective, i):  
        if findInFile(self.instanceFileLines, lambda x: ","+str(i)+"," in x): #find where subformula i appears as second operand, and 
            self.nodeCreation(lambda x: ","+str(i)+"," in x, SiConnective, i)
        elif findInFile(self.instanceFileLines, lambda x: ","+str(i)+")" in x):                   
            self.nodeCreation(lambda x: ","+str(i)+")" in x, SiConnective, i) 
        else:
            self.syntaxTree.create_node(SiConnective,str(i))
                
    def buildTree(self):
        '''
        To build the syntax tree for the formula as laid out in the instance
        file, we need to delve into the formula by means of stripping off the
        main connective of each subformula (starting with the main connective
        of the formula itself) and labeling a tree node with the symbol
        corresponding with that connective. Note that each subformula appears
        exactly once as the first argument of a tuple, and can appear at most
        once as a second (or third, for binary operators) argument in a tuple.             
        '''
        self.syntaxTree = Tree()
        
        for i in range(1, self.numTreeNodes+1):
            SiConnective = self.determineConnective(i)
            self.makeSyntaxTreeNode(SiConnective, i)
        
        #self.myShowTree(self.syntaxTree, self.syntaxTree.get_node(self.syntaxTree.root))
          
    def myShowTree(self, tree, root):
        '''
        In-order depth-first traversal of syntax tree using deep recursion; first
        layer of recursion receives root of tree, where each sub-layer receives
        respectively the left child then the right child as roots of those subtrees
        with visitation of the root node occurring in the middle.
        '''
        rootNID = root.identifier
        x=self.syntaxTree.children(rootNID)
        
        if len(self.syntaxTree.children(rootNID)) == 2:
            print("(", end=" ")
            self.myShowTree(self.syntaxTree, self.syntaxTree.children(rootNID)[0])
            
        print(self.syntaxTree.get_node(rootNID).tag, end=" ")
        
        if len(self.syntaxTree.children(rootNID)) >= 1:
            if len(self.syntaxTree.children(rootNID)) == 1:
                print("(", end=" ")
                self.myShowTree(self.syntaxTree, self.syntaxTree.children(rootNID)[0])
            else:
                self.myShowTree(self.syntaxTree, self.syntaxTree.children(rootNID)[1])
            print(")", end=" ")   
                 
'''
Testing
'''     
if __name__ == "__main__":
    #thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/needsNonReflexiveModel.I")
    #thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/implication1.I")
    thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/multipleSameAtoms.I")
    #thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/falsumTester.I")
    #thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/biconditionalTester.I")

    thing.readProblemInstanceFile()
    thing.parseProblemInstanceFile()
    thing.myShowTree(thing.syntaxTree, thing.syntaxTree.get_node(thing.syntaxTree.root))
