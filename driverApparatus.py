'''
Created on Sep 14, 2015

@author: Wanda B. Boyer
@contact: wbkboyer@gmail.com
'''

import plac

def insertRelationConditions(optionalConditionsFileName):
    '''
        Given a user-specified file
    '''

def runEnfragmo():
    '''
        Runs Enfragmo given the theory file and instance file
        
        cmd = 'vw --loss_function logistic --cache_file {} -b {} 2>&1 | tee {}'.format( 
        path_to_cache, b, tmp_log_file )
        os.system( cmd )
        output = open( tmp_log_file, 'r' ).read()
    '''

#def minimizeModel():
    
def EnfragmoOutputToKripkeStructure():
    '''
        Initially, this method will simply take the content from the runEnfragmo
        method, and will invoke the kripkeModelConstructor module on that output.
        Later, I will run Enfragmo again with a new specification file dictating
        the rules for how to 
    '''

def main(theoryFileName='~/Documents/Dropbox/Research/Final Project/Theory\ files/Single\ Modality/MLDecisionProcK.T', instanceFileName='~/Documents/Dropbox/Research/Final Project/Instance\ Files/multipleSameAtom.I',optionalConditionsFileName=''):
    "Run Enfragmo with desired Theory file and problem instance file, optionally with additional conditions."
    #print(theoryFileName+ " " + instanceFileName)
    
    if optionalConditionsFileName is not '':
        insertRelationConditions(optionalConditionsFileName)
    else:
        
    
if __name__ == '__main__':  
    plac.call(main)