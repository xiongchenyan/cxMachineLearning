'''
Created on my MAC Aug 26, 2015-8:53:11 PM
What I do:
    I am the additive kde
    assume all input dimension is independent
    estimate 1-dim kde
    pdf is \prod pdf
What's my input:

What's my output:

@author: chenyanxiong
'''




import numpy as np

from sklearn.neighbors import KernelDensity



class AdditiveKdeC(object):
    
    def __init__(self):
        self.Init()
        
        
    def Init(self):
        self.Bandwidth = 0.1
        self.lKde = None
        
        
    def SetPara(self,hPara):
        if 'bandwidth' in hPara:
            self.Bandwidth = hPara['bandwidth']
            
            
    def fit(self,lX):
        '''
        lX is the n \time d 2-D np array
        '''
        
        dim = lX.shape[1]
        
        self.lKde = [KernelDensity(bandwidth=self.Bandwidth).fit(lX[:,i]) for i in range(dim) ]
        return True
        
    
    def score(self,x):
        return self.LogPdf(x)
    
    def LogPdf(self,x):
        '''
        x is a np vector
        '''
        
        score = np.sum([self.lKde[i].score(x[i]) for i in range(x.shape[0])])
        return score
    
    def pdf(self,x):
        return np.exp(self.LogPdf(x))
            

