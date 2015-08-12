'''
Created on Aug 12, 2015 7:02:33 PM
@author: cx

what I do:
    Train ListMLE
what's my input:
    
what's my output:


'''



import itertools
from numpy.linalg.linalg import LinAlgError
import numpy as np
# import scipy
from scipy.optimize import minimize
import logging
from math import log,sqrt,pi
import json
import os,sys
from ListMLEModel import ListMLEModelC


class ListMLETrainC(object):
    
    @classmethod
    def Loss(cls, w, llQDocFeature):
        '''
        each element is a numpy array
        '''
        l = ListMLEModelC.Loss(w, llQDocFeature, cls.RankingScore)
        
        logging.info('hccrf listmle loss %f',l)
        
        return l
        
        
        


    @classmethod
    def RankingScore(cls,w,X):
        
        score = X.dot(w)
        
        return score


    @classmethod
    def Gradient(cls, theta, llGraphData):
        gf = ListMLEModelC.Gradient(theta, llGraphData, cls.RankingScore, cls.RankingScoreGradient)

        return gf
        
    
    @classmethod
    def RankingScoreGradient(cls,w,X):
        return X
    
    
            
    def Train(self,llQDocData):
        '''
        call bfgs to train
        '''
        WDim = llQDocData[0][0].shape[0]
        InitW = np.random.rand(WDim)
        
        TrainRes = minimize(self.Loss,InitW,\
                            args=(llQDocData), \
                            method='BFGS', \
                            jac=self.Gradient, \
                            options = {'disp':True, 'gtol':1e-05}
                            )
        
#         logging.info('training result message: [%s]',TrainRes.message)
        
        return TrainRes.x

