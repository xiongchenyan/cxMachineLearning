'''
Created on Jul 13, 2015 4:04:22 PM
@author: cx

what I do:
    I extract textual similarity features for LeToR
what's my input:
    qid,query,doc
what's my output:
    hFeatures (IR fusion)
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from LeToRFeature.LeToRFeatureExtractor import LeToRFeatureExtractorC
from IndriRelate.LmBase import LmBaseC
from IndriRelate.CtfLoader import TermCtfC
from IndriRelate.IndriInferencer import LmInferencerC
from cxBase.TextBase import TextBaseC


import logging


class LeToRTextSimFeatureExtractorC(LeToRFeatureExtractorC):
    
    
    def Init(self):
        LeToRFeatureExtractorC.Init(self)
        self.CtfCenter = TermCtfC()
        self.CtfDumpName = ""
        self.Inferencer = LmInferencerC()
        self.FeatureName = 'LeToRTextSim'
        self.lDocField = ['title','document','inlink']  #beware of definition in index
        self.lSimMetric = ['tfidf','lm','bm25','sdm','coor']
        
    def SetConf(self, ConfIn):
        LeToRFeatureExtractorC.SetConf(self, ConfIn)
        self.CtfDumpName = self.conf.GetConf('ctf')
        self.lDocField = self.conf.GetConf('docfield',self.lDocField)
        self.Prepare()
        
        
    @classmethod
    def ShowConf(cls):
        print cls.__name__
        print "ctf\ndocfield"
        
    
    def Prepare(self):        
        
        if self.CtfCenter.hTermCtf == {}:
            self.CtfCenter.Load(self.CtfDumpName)
                
        return True    
    
    
    
    
    def GetFieldsForDoc(self,doc):
        lFieldText = [TextBaseC.RawClean(doc.GetField(field)) for field in self.lDocField]
        return lFieldText
    
    
    def Process(self, qid, query, doc):
        BaseFeatureName = self.FeatureName
        hFeature = {}
        
        lDocText = self.GetFieldsForDoc(doc)
        lDocLm = [LmBaseC(text) for text in lDocText]
        
        
        for i in range(len(self.lDocField)):
            field = self.lDocField[i]
            text = lDocText[i]
            Lm = lDocLm[i]
            
            for SimMetric in self.lSimMetric:
                FeatureName = BaseFeatureName + field + SimMetric
                score = self.CalculateTextSim(query,Lm, text,SimMetric)   #the different func for sub class
                hFeature[FeatureName] = score

        return hFeature
    
    def CalculateTextSim(self,query,Lm,text,SimMetric):
        
        if SimMetric == 'tfidf':
            return self.Inferencer.TFIDF(query, Lm, self.CtfCenter)
        
        if SimMetric == 'lm':
            return self.Inferencer.InferQuery(query, Lm, self.CtfCenter)
        
        if SimMetric == 'bm25':
            return self.Inferencer.Bm25(query, Lm, self.CtfCenter)
        
        if SimMetric == 'sdm':
            return self.Inferencer.SDMQueryInfer(query, text, self.CtfCenter)
        
        if SimMetric == 'coor':
            return self.Inferencer.CoorMatch(query, Lm)
        
        logging.error('[%s] sim metric not supported',SimMetric)
        return 0
        
        
    
    
    
    
    
    
