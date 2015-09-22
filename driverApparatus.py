'''
Created on Sep 14, 2015

@author: Wanda B. Boyer
@contact: wbkboyer@gmail.com
'''

import plac
import os, subprocess
from modalSolverSuite.kripkeModelConstructor import kripkeModelConstructor


def insertRelationConditions(theoryFileDir, theoryFileName, optionalConditionsFileName):
    '''
        Given a user-specified file, creates a new Enfragmo theory file which
        includes those new conditions on the relation; these may or may not
        necessarily correspond with normal axiom characterizations.
    '''
    
    return theoryFileName
    

def runEnfragmo(theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName):
    '''
        Runs Enfragmo given the theory file and instance file
        
        Need to change number of worlds required, given in the problem instance
        file, until 2*k fails but 2*(k+1) succeeds. Later, will implement binary
        search in this range. Future research will create Enfragmo instance
        file based on the model produced, and will send that off to Enfragmo again
        to further minimize the model.
    '''
    cmdList = ['/home/wanda/Documents/Dropbox/Research/Final Project/Enfragmo', theoryFileDir+theoryFileName, instanceFileDir+instanceFileName]
    output = subprocess.Popen(cmdList, stdout=subprocess.PIPE).stdout#.communicate()
    outputFile = open(EnfragmoOutputDir+EnfragmoOutputFileName, 'w+')
    
    for line in output:
            outputFile.write(str(line).strip('b\'').strip('b\"').strip(r'\n') + '\n')

def EnfragmoOutputToKripkeStructure(instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName):
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
    else:
        print("The formula described in instance file "+instanceFileName+".I was determined to be unsatisfiable by Enfragmo, and therefore doesn't have a satisfying Kripke structure.")

def main(mainDir='/home/wanda/Documents/Dropbox/Research/Final Project/', theoryFileName='MLDecisionProcK.T', instanceFileName='runningEx', optionalConditionsFileName=''):
    "Run Enfragmo with desired Theory file and problem instance file, optionally with additional conditions."
    theoryFileDir=mainDir+r'Theory files/Single Modality/'
    instanceFileDir=mainDir+r'Instance Files/'
    
    EnfragmoOutputDir = mainDir+r"Output/"
    EnfragmoOutputFileName = instanceFileName+"Out.txt"
    instanceFileName=instanceFileName+'.I'
    
    if optionalConditionsFileName is not '':
        runEnfragmo(theoryFileDir, insertRelationConditions(theoryFileDir, theoryFileName, optionalConditionsFileName), instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName)
    else:
        runEnfragmo(theoryFileDir, theoryFileName, instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName)
        EnfragmoOutputToKripkeStructure(instanceFileDir, instanceFileName, EnfragmoOutputDir, EnfragmoOutputFileName)
    
if __name__ == '__main__':  
    plac.call(main)