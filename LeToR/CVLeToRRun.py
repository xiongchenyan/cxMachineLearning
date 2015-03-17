'''
Created on my MAC Nov 29, 2014-11:09:51 PM
What I do:
I run letor baseline for given models
What's my input:

What's my output:

@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from LeToR.CVRankSVM import CVRankSVMC
from LeToR.CVLeToR import CVLeToRC

import sys
from cxBase.Conf import cxConfC

if 2 != len(sys.argv):
    CVRankSVMC.ShowConf()
    print 'model ranksvm'
    sys.exit()
    
conf = cxConfC(sys.argv[1])
model = conf.GetConf('model')
if model == 'ranksvm':
    Model = CVRankSVMC(sys.argv[1])

Model.Process()
print "finished"