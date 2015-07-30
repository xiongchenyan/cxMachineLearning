'''
Created on Jul 13, 2015 4:25:35 PM
@author: cx

what I do:
     I am the center to call to extract LeToR features
what's my input:
    qid, query, doc
what's my output:
    hFeature


'''



import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from LeToRFeature.LeToRDocQualityFeatureExtractor import LeToRDocQualityFeatureExtractorC
from LeToRFeature.LeToRTextSimFeatureExtractor import LeToRTextSimFeatureExtractorC


import logging
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC

class LeToRFeatureExtractCenterC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.lFeatureGroup = []
        self.DocQualityExtractor = LeToRDocQualityFeatureExtractorC()
        self.TextSimExtractor = LeToRTextSimFeatureExtractorC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.lFeatureGroup = self.conf.GetConf('letorfeaturegroup', self.lFeatureGroup)
        if 'text' in self.lFeatureGroup:
            self.TextSimExtractor.SetConf(ConfIn)
        if 'docquality' in self.lFeatureGroup:
            self.DocQualityExtractor.SetConf(ConfIn)
            
        
    @classmethod
    def ShowConf(cls):
        cxBaseC.ShowConf()
        print cls.__name__
        print 'letorfeaturegroup text#docquality'
        LeToRDocQualityFeatureExtractorC.ShowConf()
        LeToRTextSimFeatureExtractorC.ShowConf()
        
    
    def Process(self,qid,query,doc):
        hFeature = {}
        
        if 'text' in self.lFeatureGroup:
            hFeature.update(self.TextSimExtractor.Process(qid, query, doc))
            
        if 'docquality' in self.lFeatureGroup:
            hFeature.update(self.DocQualityExtractor.Process(qid, query, doc))
        
        logging.debug('[%s-%s] letor feature extracted',qid,doc.DocNo)
        return hFeature
    
    
    def PipeRun(self,qid,query,lDoc):
        lhFeature = [self.Process(qid, query, doc) for doc in lDoc]
        return lhFeature
        
        
    
        
        
        