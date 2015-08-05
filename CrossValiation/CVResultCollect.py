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

def GetFileNames(InDir,PreName):
    lFName = WalkDir(InDir)
    lRes = [name for name in lFName if name.startswiths(PreName)]
    return lRes


def CombineEvaRes(lEvaInName,OutName):
    llEvaRes = [AdhocMeasureC.ReadPerQEva(InName, WithMean=False) for InName in lEvaInName]
    lEvaRes = list(itertools.chain(*llEvaRes))
    lEvaRes = AdhocMeasureC.AddMeanEva(lEvaRes)
    
    AdhocMeasureC.DumpPerQEva(OutName, lEvaRes)
    return True


def Process(InDir, PreName, OutName):
    
    lFName = GetFileNames(InDir, PreName)
    print 'loading res from\n %s' %('\n'.join(lFName))
    CombineEvaRes(lFName, OutName)
    print "done"
    return


import sys

if 4 != len(sys.argv):
    print 'collect ranking eva res'
    print '3 para: InDir + PreName + OutName'
    sys.exit()
    
    

Process(sys.argv[1], sys.argv[2], sys.argv[3])
    
    
    
    