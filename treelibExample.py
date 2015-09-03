''' 
Created on Sep 3, 2015

Minimal example to demonstrate failure in accessing root node of tree. The tree
created represents the infix formula (a + (b * c)).

@author: wandaboyer
'''
from treelib import Node, Tree

def buildTree(tree):
    tree.create_node("+", "1")  # root node
    tree.create_node("a", "2", parent="1")
    tree.create_node("*", "3", parent="1")
    tree.create_node("b", "4", parent="3")
    tree.create_node("c", "5", parent="3")
    
def verifyStructure(tree):
    print("Operands for root operator, '+':")
    print([x for x in tree.is_branch(str(1))])
    print("\n")
    
    print("Operands for child operator, '*':")
    print([x for x in tree.is_branch(str(3))])
    print("\n")
    

def myShowTree(tree, root):
    rootNID = root.identifier
    x=tree.children(rootNID)
    
    if len(tree.children(rootNID)) == 2:
        print "(",
        myShowTree(tree, tree.children(rootNID)[0])
        
    print tree.get_node(rootNID).tag,
    
    if len(tree.children(rootNID)) >= 1:
        if len(tree.children(rootNID)) == 1:
            print "(",
            myShowTree(tree, tree.children(rootNID)[0])
        else:
            myShowTree(tree, tree.children(rootNID)[1])
        print ")",
        
    
if __name__ == '__main__':  
    tree = Tree()
    buildTree(tree)
    verifyStructure(tree)
    
    # This inconsistently switches the order of the children, even though they
    # are in the correct order in the list
    #tree.show()
    #print(tree.root) # correctly returns nid of root, in this case str(1)
    print(tree.get_node(tree.root))
    myShowTree(tree, tree.get_node(tree.root))
    