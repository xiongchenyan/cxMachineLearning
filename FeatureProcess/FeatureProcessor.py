'''
Created on Jul 22, 2015 3:36:47 PM
@author: cx

what I do:
i process features
     like in hFeature format
what's my input:

what's my output:


'''

import logging
import sys
import numpy

class FeatureProcessorC(object):
    
    @classmethod
    def Max(cls,hA,hB):
        hMax = dict(hA)
        for key,score in hB.items():
            if key in hMax:
                hMax[key] = max(hMax[key],score)
            else:
                hMax[key] = score
                
        return hMax
    
    
    @classmethod
    def Min(cls,hA,hB):
        hMin = dict(hA)
        for key,score in hB.items():
            if key in hMin:
                hMin[key] = min(hMin[key],score)
            else:
                hMin[key] = score
                
        return hMin
    
    
    @classmethod
    def MaxMinNormalization(cls,hFeature,hMax,hMin):
        hRes = {}
        for key,score in hFeature.items():
            if (not key in hMax) | (not key in hMin):
                hRes[key] = score
                continue
            
            MaxScore = hMax[key]
            MinScore = hMin[key]
            
            if MaxScore == MinScore:
                score = 0
            else:
                score = (score - MinScore) / float(MaxScore - MinScore)
            hRes[key] = score
        return hRes
    
    @classmethod
    def IntlizeFeatureName(cls,hFeature,hFeatureId):
        hRes = {}
        
        for key,score in hFeature.items():
            if not key in hFeatureId:
                logging.error('%s: feature [%s] not in id list',cls.__name__,key)
                sys.exit()
                
            hRes[hFeatureId[key]] = score
        return hRes
    
    
    @classmethod
    def VectorlizeFeature(cls,hFeature,hFeatureId,FeatureDim = 0):
        if 0 == FeatureDim:
            FeatureDim = len(hFeatureId)
            
        V = numpy.zeros(FeatureDim)
        for key,score in hFeature.items():
            if not key in hFeatureId:
                logging.error('%s: feature [%s] not in id list',cls.__name__,key)
                sys.exit()
            
            V[hFeatureId[key]] = score
        return V
            
            
        
        
        
        
        
        
        
        
        
        