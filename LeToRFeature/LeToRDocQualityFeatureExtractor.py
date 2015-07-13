'''
Created on Jul 13, 2015 3:55:07 PM
@author: cx

what I do:
    extract doc quality features
what's my input:
    qid,query,doc
what's my output:
    hFeature

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from IndriSearch.IndriDocBase import IndriDocBaseC
from LeToRFeature.LeToRFeatureExtractor import LeToRFeatureExtractorC
from cxBase.base import cxConfC
from cxBase.base import cxBaseC
from IndriRelate.LmBase import LmBaseC
import logging

class LeToRDocQualityFeatureExtractorC(LeToRFeatureExtractorC):
    
        
    def Init(self):
        LeToRFeatureExtractorC.Init(self)
        self.FeatureName = 'LeToRDocQuality'
        self.hSpamScore = {}
        self.SpamInName = ""
        
    def SetConf(self, ConfIn):
        LeToRFeatureExtractorC.SetConf(self, ConfIn)
        self.SpamInName = self.conf.GetConf('spamscore')
        self.Prepare()
        logging.info('doc quality feature conf setted')
        
       
    @staticmethod
    def ShowConf():
        LeToRFeatureExtractorC.ShowConf()
        print "spamscore"
        
    
    def Prepare(self):
        if "" != self.SpamInName:
            logging.info("load spam score from [%s]" %(self.SpamInName))
            for line in open(self.SpamInName):
                vCol = line.strip().split()
                if len(vCol) < 2:
                    logging.warn("[%s] format error" %(line))
                    continue
                self.hSpamScore[vCol[0]] = vCol[1]
        
        
    def Process(self, qid,query,doc):
        hFeature = {}
        hFeature.update(self.ExtractUrlLen(doc))
        hFeature.update(self.ExtractOOVFrac(doc))
        hFeature.update(self.ExtractIsWiki(doc))
        hFeature.update(self.ExtractSpamScore(doc))
        hFeature.update(self.ExtractDocLen(doc))
        hFeature.update(self.ExtractInlinkCnt(doc))
        self.hDocFeature[doc.DocNo] = hFeature
        return hFeature
    
    def ExtractDocLen(self,doc):
        score = len(doc.GetContent().split())
        return {self.FeatureName + 'DocLen':score}
    
    def ExtractSpamScore(self,doc):
        score = 0
        if doc.DocNo in self.hSpamScore:
            score = int(self.hSpamScore[doc.DocNo])
        return {self.FeatureName + 'SpamScore':score}
        
        
    def ExtractUrlLen(self,doc):
        UrlStr = doc.GetField('url')
        hFeature = {}
        hFeature[self.FeatureName + 'urllen'] = len(UrlStr.split())
        return hFeature
    
    def ExtractOOVFrac(self,doc):
        hFeature = {}
        Lm = LmBaseC(doc)
        score = Lm.GetTFProb('[OOV]') + Lm.GetTFProb('[oov]')
        hFeature[self.FeatureName + 'OOVFrac'] = score
        return hFeature
    
    def ExtractIsWiki(self,doc):
        UrlStr = doc.GetField('url')
        score = 0
        if 'wikipedia' in UrlStr:
            score = 1
        return {self.FeatureName + 'IsWiki':score}
         
    def ExtractInlinkCnt(self,doc):
        score = 0
        doc.SetHField()
        if 'inlink' in doc.hField:
            score = len(doc.hField['inlink'])
        return {self.FeatureName + 'InlinkCnt':score}    
    
