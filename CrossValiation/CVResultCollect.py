'''
Created on Aug 5, 2015 10:08:56 AM
@author: cx

what I do:

what's my input:

what's my output:


'''

import subprocess

import site
import itertools
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
import ntpath
from cxBase.WalkDirectory import WalkDir

def GetFileNames(InDir,PreName,k):
#     lFName = WalkDir(InDir)
#     lRes = [name for name in lFName if ntpath.basename(name).startswith(PreName)]
    lRes = [PreName + '_%d' %(i) for i in range(k)]
    
    return lRes


def CombineEvaRes(lEvaInName,OutName):
    llEvaRes = [AdhocMeasureC.ReadPerQEva(InName, WithMean=False) for InName in lEvaInName]
    lEvaRes = list(itertools.chain(*llEvaRes))
    lEvaRes = AdhocMeasureC.AddMeanEva(lEvaRes)
    
    AdhocMeasureC.DumpPerQEva(OutName, lEvaRes)
    print ntpath.basename(OutName) + ': ' + lEvaRes[-1][1].dumps()
    return True


def Process(InDir, PreName, OutName,k):
    
    lFName = GetFileNames(InDir, PreName,k)
#     print 'loading res from\n %s' %('\n'.join(lFName))
    CombineEvaRes(lFName, OutName)
#     print "done"
    return


import sys

if 4 > len(sys.argv):
    print 'collect ranking eva res'
    print '3 or 4 para: InDir + PreName + OutName + k(10)'
    sys.exit()
    
    
k = 10
if len(sys.argv) > 4:
    k= int(sys.argv[4])

Process(sys.argv[1], sys.argv[2], sys.argv[3],k)
    
    
    
    