'''
Created on Jul 13, 2015 3:44:16 PM
@author: cx

what I do:
    I am the base class for letor feature extraction
what's my input:
    qid,query + doc (IndriDocBaseC)
what's my output:
    hFeature = {name:score}


'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from IndriSearch.IndriDocBase import IndriDocBaseC

from cxBase.base import cxConfC
from cxBase.base import cxBaseC

import logging

class LeToRFeatureExtractorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        
        
    def Process(self,qid,query,doc):
        logging.error('call my subclasses ',self.__name__)
        return {}
        
        
    def PipelineRun(self,qid,query,lDoc):
        lhFeature = [self.Process(qid, query, doc) for doc in lDoc]
        return lhFeature
        
        
        


    
        
        

