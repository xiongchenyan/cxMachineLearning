'''
Created on Jun 12, 2014
The naive bayesian classifier
@author: cx
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from IndriRelate.IndriInferencer import LmBaseC
from cxBase.TextBase import *
class NaiveBayesianClassifierC(cxBaseC):
    def Init(self):
        self.lLm = []
        self.lDomain = []
        self.hDomain = {}
        self.DomainLevel = 1
        self.lStopDomain = ['/user','/common','/m','/imdb','/nytimes','/wikipedia','/pipeline'] 
        self.bReduceSize = True
        
        
    def CateLoader(self,RawStr):
        vCol = RawStr.strip('/').split('/')
        res = '/' + '/'.join(vCol[:self.DomainLevel])
        return res
        
    def Train(self,InName):
        cnt = 0
        for line in open(InName):
            vCol = line.strip().split('\t')
            if len(vCol) < 2:
                continue
            cate = self.CateLoader(vCol[0])
            if cate in self.lStopDomain:
                continue
            text = TextBaseC.RawClean(vCol[1])
            if not cate in self.hDomain:
                p = len(self.lDomain)
                self.lDomain.append(cate)
                self.lLm.append(LmBaseC())
                self.hDomain[cate] = p
            else:
                p = self.hDomain[cate]
            self.lLm[p].AddRawText(text)       
            cnt += 1
            if 0 == (cnt % 1000):
                print "[%d] line [%d] cate" %(cnt,len(self.lDomain)) 
        if self.bReduceSize:
            self.ReduceSize()
        return True
    
    
    def ReduceSize(self):
        self.DiscardLowFreqTerm()
#         self.DiscardAverageTerm()
        
    def DiscardLowFreqTerm(self):
        for Lm in self.lLm:
            hNew = dict(Lm.hTermTF)
            for item,value in hNew:
                if value < 2:
                    del Lm.hTermTF[item]
            Lm.CalcLen()
    
    
    
    def dump(self,OutName):
        out = open(OutName,'w')
        for i in range(len(self.lDomain)):
            print >>out, self.lDomain[i] + '\t' + self.lLm[i].dumps()
        out.close()
        return
    
    
    def load(self,InName):
        for line in open(InName):
            vCol = line.strip().split('\t')
            if vCol[0] in self.lStopDomain:
                continue
            self.lDomain.append(vCol[0])
            self.hDomain[vCol[0]] = len(self.lDomain) - 1
            lm = LmBaseC()
            lm.loads('\t'.join(vCol[1:]))
            self.lLm.append(lm)
        if self.bReduceSize:
            self.ReduceSize()
        return
    
    
    def Predict(self,text):
        #add one smoothing
        lProb = [0] * len(self.lDomain)
        lTerm = TextBaseC.RawClean(text).split()
        Sum = 0
        
        for term in lTerm:
            for i in range(len(self.lLm)):
                prob = self.lLm[i].GetTFProb(term)
                lProb[i] += prob
                
        Total = sum(lProb)
        if 0 == Total:
            return [1.0/len(self.lDomain)] * len(self.lDomain)
        
        lProb = [item/Total for item in lProb]
        return self.lDomain,lProb