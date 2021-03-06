'''
Created on Aug 17, 2015 4:35:32 PM
@author: cx

what I do:
    I implement gradient optimization method
what's my input:
    follow from scipy.optimize import minimize API
what's my output:
    follow minimize API

'''



import numpy as np
import logging


class GradientResC(object):
    
    def __init__(self):
        self.x = 0
        self.fun = np.zeros(1)

class GradientMethodC(object):
    
    def GradientDecent(self,LossFunc, InitW, Para, GradientFunc, ConvergeThreshold):
        '''
        typical gradient method
        LossFunc takes w,Para[0] as parameter, return a float as loss
        GradientFunc has same parameter, return gradients
        InitW is initial parameter
        ConvergeThreshold is the change rate on LOSS FUNCTION as termination condition
        '''
        
        
        w = np.array(InitW)
        LastLoss = LossFunc(w,Para)
        MaxIte = 1000
        StepSize = 0.005
        DecayRate = 0.5
        
        logging.info('start with w: %s',np.array2string(w))
        logging.info('start loss: %f',LastLoss)
        for Ite in range(MaxIte):
            
            Gw = GradientFunc(w,Para)
            
            ThisW = w - StepSize * Gw
            logging.info('Gw:\n%f',np.array2string(Gw))
            logging.info('NewW:\n%f',np.array2string(w))
            ThisLoss = LossFunc(ThisW,Para)
            logging.info('step [%d] loss [%f]',Ite,ThisLoss)
            if ThisLoss > LastLoss:
                StepSize *= DecayRate
                logging.info('hurt, decay stepsize to %f',StepSize)
                continue
            
            
            ChangeRate = np.abs ( (ThisLoss - LastLoss) / LastLoss)

            LastLoss = ThisLoss
            w = ThisW
            
            if ChangeRate < ConvergeThreshold:
                logging.info('Change Rate [%f < %f], converged',ChangeRate,ConvergeThreshold)
                break
        
        res = GradientResC()
        res.x = w
#         res.fun = np.array([LastLoss])
        res.fun = LastLoss    
        return res
                  
            