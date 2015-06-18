'''
Created on Jun 12, 2015

@author: wandaboyer
'''
import re

class formulaConversion(object):
    '''
    This module is meant to convert the modal benchmark formulas from the Logic
    Work Bench (http://iamwww.unibe.ch/~lwb/benchmarks/benchmarks.html) into
    a usable form.
    '''

    def __init__(self, filepath, inputFileName, outputDir):
        '''
        Receives the name of the modal benchmark formula file to be converted.
        '''
        self.filepath = filepath
        self.fileName = inputFileName
        self.outputDir = outputDir   
        
    def readBenchmarkFile(self):
        '''
        This method assumes that the file exists and is correctly formatted. The
        file begins with a line containing the filename, followed by the
        delimiter 'begin'; these lines are to be deleted. Each file contains 
        multiple formulas, delimited by the character group '$n:', where $n 
        stands for the formula's index number; in the generated file, each line
        will contain a single formula (sans index number).
        '''
        self.benchmarkFileLines = [line.strip().split(':')[-1] for line in open(self.filepath) if line != '\n']
        
        # Removes first and second lines, which correspond to filename and begin
        # Alternately, using list slicing: self.benchmarkFileLines = self.benchmarkFileLines[2:]
        del self.benchmarkFileLines[0:2]
    
    def parseBenchmarkFile(self):
        '''
        In order to facilitate ease of use with Megan's parser, the atom naming
        convention must be changed so as to strip out the preceding 'p' for each
        instance of an atom. Then, a space will be added between each token.
        '''
        self.stripAtomNaming()
        self.correctSpacing()

    def stripAtomNaming(self):
        '''
        This method simply strips every occurrence of 'p' from the benchmark
        formulas, since the labeling is otherwise unique. While maintaining
        the string of one or more digits ('\2' refers to '\d+' in the first arg
        to re.sub), we add an additional space; this requires removing the space
        that existed previously before each '->' and '&', but it all comes out
        in the wash. If only they'd been more consistent with their spacing in 
        the first place!
        '''
        self.benchmarkFileLines = [re.sub(r'(p)(\d+)', r'\2 ', formula) for formula in self.benchmarkFileLines]
        
    def correctSpacing(self):
        self.benchmarkFileLines = [self.multiple_replace(formula, {'box':'box ', 'dia':'dia ', '~':'~ ', '(':'( ', ')':') ', ' ->':'->', ' &':'&'}) for formula in self.benchmarkFileLines]
        
    def multiple_replace(self, string, rep_dict):
        pattern = re.compile("|".join([re.escape(k) for k in rep_dict.keys()]), re.M)
        return pattern.sub(lambda x: rep_dict[x.group(0)], string)
    
    def printNewBenchmarkFile(self):
        outputFile = open(self.outputDir+self.fileName+'-Modified.txt', 'w+')
        
        for formula in self.benchmarkFileLines:
            outputFile.write("%s\n" % formula.strip())

'''
Testing
'''     
if __name__ == "__main__":
    inputDir = "/home/wanda/Documents/Dropbox/Research/Modal benchmark formulas/"
    inputFileName = "k_branch_n"
    outputDir = inputDir+"ModifiedFormulas/"
    
    thing = formulaConversion(inputDir+inputFileName+'.txt', inputFileName, outputDir)
    thing.readBenchmarkFile()
    thing.parseBenchmarkFile()
    thing.printNewBenchmarkFile()