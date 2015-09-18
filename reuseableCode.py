'''
Created on Sep 17, 2015

@author: Wanda B. Boyer
@contact: wbkboyer@gmail.com
'''
#from collections import __main__
from collections import defaultdict
import re

from functools import partial
from sre_parse import Pattern

'''def findInFile(fileLines, predicate):
        i = 0
        for x in fileLines:
            if predicate(x):
                    return i
            i+=1
'''
def findInFile(fileLines, predicate, startIndex=0):
    for i, x in enumerate(fileLines,start=startIndex):
        if predicate(x):
            return i

def findRegexLine(fileLines, regexToMatch):
    for i, x in enumerate(fileLines):
        if re.match(regexToMatch, x):
            return i
        

def extractTuples(fileLines, relationName):
    tupleDict = defaultdict(list)
    #toMatch = re.compile('(<DataSet Name=)(\s?)(\'\")'+re.escape(relationName))
    toMatch = re.compile('<DataSet Name=\s?\'\"{bla}'.format(bla=relationName))
    startIndex = findRegexLine(fileLines, toMatch)
    #startIndex = findInFile(fileLines, lambda x: "<DataSet Name='Accessible" in x)
    endingIndex = findInFile(fileLines, lambda x: "</DataSet>" in x, startIndex+1)

    relationLines = fileLines[startIndex+1:endingIndex-startIndex-1]

    for line in relationLines:
        print(line)
        line = line.split('\'/><IntValue Name= \'')
        line = [line[0][-1], line[1][0]]
        tupleDict[line[0]].append(line[1])
    
if __name__ == "__main__":
    fileLines = ["<PredicateInfo>","<PredicateSymbol><BasicInfo Name='Accessible' IsGiven= '1' ToBePrinted= '0'/><TypeInfoCollection><IntTypeInfo Name='World'/><IntTypeInfo Name='World'/></TypeInfoCollection></PredicateSymbol>","<DataSet Name='Accessible' TypeSize= '2' >","<ARow><IntValue Name= '1'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '2'/><IntValue Name= '1'/><True/></ARow>","</DataSet>","</PredicateInfo>"]
    extractTuples(fileLines, "Accessible")