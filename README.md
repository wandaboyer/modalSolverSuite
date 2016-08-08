# The Modal Solver Suite
## An implementation of a Decision and Minimization Procedure for Modal Logic

This repository containts the Python modules that comprise the Modal Solver Suite.

### Modules 
1. driverObj.py 
    
    The main module, which contains the decision and minimization procedure, and invokes the Kripke model constructor.  

1. kripkeModelConstructor.py 

    Parses the output from Enfragmo to produce a .dot file and .svg file for each model.  

1. verifier.py

    Parses problem instance files and returns the formula represented by the file in infix notation.

1. reuseableCode.py

    Various code snippets used in multiple modules.  

1. formulaConversion.py 

    This module is meant to convert the modal benchmark formulas from the [Logic Work Bench](http://iamwww.unibe.ch/~lwb/benchmarks/benchmarks.html) into a usable form. 


### Dependencies The Modal Solver Suite requires the following Python modules to function: 
1. [Union Find](https://github.com/wandaboyer/Algorithms.git) (branch of Algorithms repository that includes setup.py)
1. [Graphviz](https://github.com/xflr6/graphviz.git) - tested with v0.4.10
1. [Treelib](https://github.com/caesar0301/treelib.git) - tested with v1.3.3 - commit 65635f4
1. [Plac](https://pypi.python.org/pypi/plac)
1. [Re](https://docs.python.org/3/library/re.html)
1. [Os](https://docs.python.org/3/library/os.html)
1. [Defaultdict](https://docs.python.org/3.3/library/collections.html#collections.defaultdict)

It is recommended that you create a (virtual environment)[http://docs.python-guide.org/en/latest/dev/virtualenvs/] with the Python 3.4 interpreter and these modules.

If you have not already done so, please clone the following repo:

   [Supplementary Files](https://github.com/wandaboyer/MSS-SupplementaryFiles.git) 

Which contains the theory file for the modal logic K, sample problem instance files, and some examples of first-order frame correspondents.
