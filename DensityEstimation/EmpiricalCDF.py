'''
Created on May 27, 2014
F(x) = 1/n \sum_i I(x_i < x)
@author: cx
'''

import json
import math
class EmpiricalCDFC(object):
    def Init(self):
        self.lCdfSpliter = []
        self.InterValNum = 100 #%1 default
        
        
    def __init__(self):
        self.Init()
        
    def Make(self,lNum):
        lNum.sort()
        for i in xrange(0,len(lNum),self.InterValNum):
            self.lCdfSpliter.append(lNum[i])
            
    def GetCdf(self,num):
        p = 0
        for i in range(len(self.lCdfSpliter)):
            if num > self.lCdfSpliter[i]:
                p = i + 1
                break
        cdf = min(1.0,1.0/self.InterValNum * p)
        return cdf
    
    def dumps(self):
        return str(self.InterValNum) + '\t' +  json.dumps(self.lCdfSpliter)
    
    def loads(self,line):
        vCol = line.split('\t')
        self.InterValNum = int(vCol[0])
        self.lCdfSpliter = json.loads(vCol[1])
        return True
    
    
        
    
        