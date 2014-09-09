'''
Created on Sep 9, 2014
show top terms of each category to have a look
for each term in Nb Classifier's Lm
    get its probability
output the top terms (in predicted probability) for each class
@author: cx
'''

from NaiveBayesianClassifier import *
import sys



if 3 != len(sys.argv):
    print "get top terms for each class: nb dump + out"
    sys.exit()
    
NbClassifier = NaiveBayesianClassifierC()
NbClassifier.load(sys.argv[1])


out = open(sys.argv[2],'w')

for i in range(len(NbClassifier.lLm)):
    res = NbClassifier.lDomain[i]
    lThisClassTerm = []
    for term in NbClassifier.lLm[i].hTermTF.keys():
        lProb = NbClassifier.Predict(term)[1]
        prob = lProb[i]
        lThisClassTerm.append([term,prob])
    lThisClassTerm.sort(key=lambda item:item[1],reverse = True)
    lMid =[item[0] + ':%f'%(item[1]) for item in lThisClassTerm]
    res += '\t' + '\t'.join(lMid)
    print >>out, res
    
    
out.close()    