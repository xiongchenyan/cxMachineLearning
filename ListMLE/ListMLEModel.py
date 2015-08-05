'''
Created on Aug 5, 2015 1:30:12 PM
@author: cx

what I do:
    I contain the function need for training ListMLE
        testing will be extremely easy, could be done by LeToR's class generally (TBD)
    Aug 5 2015:
        provide listwise loss and gradient for any function that
             provide ranking function f
             and gradients f'
what's my input:
    
what's my output:


'''

import numpy as np
# import scipy
# from scipy.optimize import minimize
import logging
from math import log


class ListMLEModelC(object):
    
    @classmethod
    def Loss(cls,w,llQDocData,f):
        '''
        w is the parameter, one dim np array
        llQDocData is a two dimension array, first is q, second is doc,
            its element can be anything
            the only requirement is that it has a GetRelScore() function to return relevance score of doc
        f is the ranking function, takes w and each element in llQDocData as input, and return a ranking score
        
        return a (average of ) listwise loss value for llQDocData and w
        '''
        
        l = np.mean([cls.PerQLoss(w,lQDocData,f) for lQDocData in llQDocData])
        logging.info('loss %f',l)
        return l
    

    @classmethod
    def PerQLoss(cls,w,lQDocData,f):
        '''
        the loss for each q
        '''
        loss = 0
        #get optimal order
        lQDocData.sort(key=lambda item:item.GetRelScore(), reverse = True)
        
        lRankingScore = [f(w,data) for data in lQDocData]  #local prediction assumption
        lExpF = np.exp(lRankingScore)
        SumExpF = np.sum(lExpF)
        CurrentSum = SumExpF
        for i in range(len(lRankingScore)):
            ThisDocLoss = -lRankingScore[i] + log(CurrentSum)
            CurrentSum -= lExpF[i]
            
            loss += ThisDocLoss
            
        return loss
            
        
        
        
    
    
    
    
    @classmethod
    def Gradient(cls,w,llQDocData,f,gf):
        '''
        w is the parameter, one dim np array
        llQDocData is a two dimension array, first is q, second is doc,
            its element can be anything
            the only requirement is that it has a GetRelScore() function to return relevance score of doc
        
        f is the ranking function, takes w and each element in llQDocData as input, and return a ranking score
        
        gf is the gradient function, takes w and each element in llQDocData as input, return gradient respect to ranking score
        
        return the listwise gradient for llQDocData and w (one dimension array)
        '''
        
        
        res = np.mean([cls.PerQGradient(w,lQDocData,f,gf) for lQDocData in llQDocData],0)

        logging.debug('gradient %s',np.array2string(gf))        
        return res
    
    
    @classmethod
    def PerQGradient(cls,w,lQDocData,f,gf):
        
        res = np.zeros(w.shape)
        
        #optimal order
        lQDocData.sort(key=lambda item:item.GetRelScore(),reverse = True)
        
        
        
        lPerDocGf = np.array([gf(w,data) for data in lQDocData])  #|doc| * |w| mtx
        lExpF = np.exp([f(w,data) for data in lQDocData])

        MultiWeightMtx = lExpF.reshape([len(lExpF),1]).dot( np.ones([1,res.shape[0]]) )  #reshape for dot product 
        lExpFWeightedGf = lPerDocGf * MultiWeightMtx
            
        SumExpF = np.sum(lExpF)
        SumWeightedGf = np.sum(lExpFWeightedGf,0)
        
        for i in range(len(lQDocData)):
            res = -lPerDocGf[i,:] + SumWeightedGf / SumExpF
            SumExpF -= lExpF[i]
            SumWeightedGf -= lExpFWeightedGf[i,:]
            
        return res
        
        
        
        
        
        
        
        
        
        
    
    
   
   
   