'''
Created on Jan. 12, 2015

@author: Wanda B. Boyer
@contact: wbkboyer@gmail.com
'''
from treelib import Tree, Node
import re

class verifier:
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
        self.SameAtomList = []
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
        self.setUpSameAtomList() #NEW
        self.buildTree()
        self.printFormula()
     
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
            
    def findInInstanceFile(self, predicate):
        i = 0
        for x in self.instanceFileLines:
            if predicate(x):
                    return i
            i+=1
      
    def assignSymbol(self, label):
        if label == "And":
            return "&"
        elif label == "Or":
            return "v"
        elif label == "Not":
            return "~"
        elif label == "Implication":
            return "->"
        elif label == "Box":
            return "box"
        elif label == "Diamond":
            return "dia"
        
    ''' def assignAtom(self, i): #this appears to be fucked.
        if len(self.SameAtomList) == 0:
            self.SameAtomList.append(str(i)) # Adds subformula label for the atom to the list
            return "p"+str(1)
        else:
            for x in self.SameAtomList: #For each list of subformulas corresponding to same atom
                #if x.contains(str(i)): #if we see the subformula is already in a list element, then we must have already realized that it refers to the same atom as another subformula
                if str(i) in x:
                    return "p"+str(x.index()+1) # return the label for the atom; need 1-indexed labeling
                else:
                    self.SameAtomList.append(str(i)) # since you haven't seen the atom before, add it as another label
                    return "p"+str(len(self.SameAtomList)) #need the index of the most recent addition
    '''
    def assignAtom(self, i):
        j = 1
        for atomEquivClass in self.SameAtomList:
            if str(i) in atomEquivClass:
                return str(j)
            j += 1
        
    def setUpSameAtomList(self):
        startIndex = self.findInInstanceFile(lambda x: "PREDICATE SameAtom" in x) + 1

        sameAtomPairs = self.instanceFileLines[startIndex:]
        
        for pair in sameAtomPairs:
            tmp = pair.split(",")
            label1 = tmp[0].split("(")[1]
            label2 = tmp[1].split(")")[0]
            
            if not self.SameAtomList:
                self.SameAtomList.append(set())
                
            for atomEquivClass in self.SameAtomList:
                if label1 in atomEquivClass:
                    atomEquivClass.add(label2)
                elif label2 in atomEquivClass:
                    atomEquivClass.add(label1)
                elif not atomEquivClass:
                    atomEquivClass.add(label1)
                    atomEquivClass.add(label2)
        
    def determineConnective(self, i):
        '''
            Each subformula label is guaranteed to be the first argument of some
            tuple; either it will correspond with an atom, the only argument,
            or it will correspond with the main connective of a unary 
            (i.e. negation, box, or diamond) or binary (i.e. conjunction or 
            disjunction) subformula.
            '''
        if self.findInInstanceFile(lambda x: "("+str(i)+")" in x):
            return self.assignAtom(i)
        if self.findInInstanceFile(lambda x: "("+str(i)+"," in x):
            SiAsMainConnective = self.findInInstanceFile(lambda x: "("+str(i)+"," in x)
            for j in range(SiAsMainConnective, 0, -1): # go back in the file until you can find out what predicate we're dealing with
                if self.instanceFileLines[j].split(" ")[0] == "PREDICATE":
                    if self.instanceFileLines[j].split(" ")[1] == "SameAtom": # if there are no tuples under SameAtom, then this isn't reached due to SiAsMainConnective
                        return self.assignAtom(i)
                    else:
                        return self.assignSymbol(self.instanceFileLines[j].split(" ")[1]) # if the predicate refers to an operator, then we need to find out which one!
    
    def nodeCreation(self, predicate, SiConnective, i):        
        SiAsFirstOperand = self.findInInstanceFile(predicate)
        ParentOfSi = str(self.instanceFileLines[SiAsFirstOperand].split(",")[0].split("(")[1])
        self.syntaxTree.create_node(SiConnective, str(i), parent=ParentOfSi)
        
    def makeSyntaxTreeNode(self, SiConnective, i):   
        if self.findInInstanceFile(lambda x: ","+str(i)+"," in x):
            self.nodeCreation(lambda x: ","+str(i)+"," in x, SiConnective, i)
        elif self.findInInstanceFile(lambda x: ","+str(i)+")" in x):                   
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
          
        self.syntaxTree.show()
        
    def printFormula(self):
        oplist = []
        formula = ""
        bracketcount = 0
        atomLabelRegex = re.compile(r'\d+')
        for x in self.syntaxTree.expand_tree(mode=Tree.DEPTH, reverse=True):
            #if "\d+" in self.syntaxTree[x].tag:
            if atomLabelRegex.search(self.syntaxTree[x].tag) is not None:
                tmp = self.syntaxTree[x].tag
                while oplist.__len__()>0:
                    currOp = oplist.pop()
                    if currOp in ["box", "dia"]:
                        tmp = currOp + " ( " + tmp + " )"
                    elif currOp in ["~"]:
                        tmp = currOp + " " + tmp
                    elif currOp in ["v", "&", "->"]:
                        tmp = "( " + tmp + " " + currOp  + " "
                        bracketcount += 1
                        break
                formula += tmp
            elif self.syntaxTree[x].tag in ["~", "box", "dia"]:
                oplist.append(self.syntaxTree[x].tag)
            elif self.syntaxTree[x].tag in ["v", "&", "->"]:
                oplist.append(self.syntaxTree[x].tag)
        while bracketcount > 0:
                    formula += " )"
                    bracketcount -= 1        
        print(formula)
'''
Testing
'''     
if __name__ == "__main__":
    thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/needsNonReflexiveModel.I")
    #thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/implication1.I")
    #thing = verifier("/home/wanda/Documents/Dropbox/Research/Final Project/Instance Files/multipleSameAtoms.I")
    thing.readProblemInstanceFile()
    thing.parseProblemInstanceFile()