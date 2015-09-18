'''
Created on Sep 17, 2015

@author: Wanda B. Boyer
@contact: wbkboyer@gmail.com
'''
from collections import defaultdict
import re

def findInFile(fileLines, predicate, startIndex=0):
    for i, x in enumerate(fileLines[startIndex:]):
        if predicate(x):
            return startIndex+i

def findRegexLine(fileLines, regexToMatch):
    for i, x in enumerate(fileLines):
        if re.search(regexToMatch, x) is not None:
            return i 

def extractTuples(fileLines, relationName):
    opDict = defaultdict(list)
    toMatch = re.compile(r'''<DataSet Name=\s?'{bla}'''.format(bla=relationName))
    startIndex = findRegexLine(fileLines, toMatch)
    endIndex = findInFile(fileLines, lambda x: "</DataSet>" in x, startIndex+1)

    relationLines = fileLines[startIndex+1:endIndex]
    for line in relationLines:
        firstElem = line.split('\'/><IntValue Name= \'')[0].strip('<ARow><IntValue Name= \'')
        secondElem= line.split('\'/><IntValue Name= \'')[1].strip('\'/><True/></ARow>')
        if relationName is 'TrueAt':
            opDict[secondElem].append(firstElem)
        else:
            opDict[firstElem].append(secondElem)
    return opDict
if __name__ == "__main__":
    fileLines = ["<PredicateInfo>","<PredicateSymbol><BasicInfo Name='TrueAt' IsGiven= '1' ToBePrinted= '0'/><TypeInfoCollection><IntTypeInfo Name='Subformula'/><IntTypeInfo Name='World'/></TypeInfoCollection></PredicateSymbol>","<DataSet Name= 'TrueAt' TypeSize= '2' >","<ARow><IntValue Name= '1'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '1'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '2'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '2'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '3'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '3'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '4'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '4'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '5'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '5'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '6'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '6'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '7'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '7'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '10'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '10'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '11'/><IntValue Name= '1'/><True/></ARow>","<ARow><IntValue Name= '12'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '13'/><IntValue Name= '1'/><True/></ARow>","</DataSet>","</PredicateInfo>","<PredicateInfo>","<PredicateSymbol><BasicInfo Name='Accessible' IsGiven= '1' ToBePrinted= '0'/><TypeInfoCollection><IntTypeInfo Name='World'/><IntTypeInfo Name='World'/></TypeInfoCollection></PredicateSymbol>","<DataSet Name='Accessible' TypeSize= '2' >","<ARow><IntValue Name= '1'/><IntValue Name= '2'/><True/></ARow>","<ARow><IntValue Name= '2'/><IntValue Name= '1'/><True/></ARow>","</DataSet>","</PredicateInfo>"]
    extractTuples(fileLines, "TrueAt")