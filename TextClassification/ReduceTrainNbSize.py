'''
Created on Jun 12, 2014
reduce the size of trained naive bayesian classifier
@author: cx
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from TextClassification.NaiveBayesianClassifier import *

import sys

if 3 != len(sys.argv):
    print "2 para: trained lm set + out reduced lm set"
    sys.exit()
    
    
NbClassifier = NaiveBayesianClassifierC()
NbClassifier.load(sys.argv[1])
NbClassifier.dump(sys.argv[2])
