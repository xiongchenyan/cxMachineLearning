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

class ListMLEDocC(object):
    def __init__(self):
        self.X = np.zeros([0,0])
        self.rel = 0
        self.DocNo = ""
    
    def GetRelScore(self):
        return self.rel

class ListMLETrainC(object):
    
    @classmethod
    def Loss(cls, w, llQDocData):
        '''
        each element is a numpy array
        '''
        l = ListMLEModelC.Loss(w, llQDocData, cls.RankingScore)
        
        logging.info('hccrf listmle loss %f',l)
        
        return l
        
        
        


    @classmethod
    def RankingScore(cls,w,DocData):
        
        score = DocData.X.dot(w)
        
        return score


    @classmethod
    def Gradient(cls, theta, llQDocData):
        gf = ListMLEModelC.Gradient(theta, llQDocData, cls.RankingScore, cls.RankingScoreGradient)

        return gf
        
    
    @classmethod
    def RankingScoreGradient(cls,w,DocData):
        return DocData.X
    
    
            
    def Train(self,llQDocData,method='BFGS',ConvergeThreshold=1e-05):
        '''
        call bfgs to train
        '''
        WDim = llQDocData[0][0].X.shape[0]
        InitW = np.random.rand(WDim)
        
        TrainRes = minimize(self.Loss,InitW,\
                            args=(llQDocData), \
                            method=method, \
                            jac=self.Gradient, \
                            options = {'disp':True, 'gtol':ConvergeThreshold}
                            )
        
#         logging.info('training result message: [%s]',TrainRes.message)
        
        return TrainRes.x

