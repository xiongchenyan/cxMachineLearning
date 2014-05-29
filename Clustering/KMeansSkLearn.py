'''
Created on May 28, 2014
kmean API via me

prefer matlab...

@author: cx
'''


from time import time
import numpy as np
import pylab as pl

from sklearn import metrics
from sklearn.cluster import KMeans

from cxBase.base import cxBaseC,cxConf

class cxKMeansSkLearnC(cxBaseC):
    def Init(self):
        self.k = 8
        self.InName = ""
        self.OutName= ""
        self.data = []
        self.lLabel = []
    
    @staticmethod
    def ShowConf():
        print "k\nin\nout"
        
    def SetConf(self,ConfIn):
        conf = cxConf(ConfIn)
        self.k = int(conf.GetConf('k', self.k))
        self.InName = conf.GetConf('in')
        self.OutName = conf.GetConf('out')
        
    def LoadData(self):
        #could be re-implemented
        
        l = []
        for line in open(self.InName):
            vCol = line.strip().split()
            l.append([int(item) for item in vCol])
        
        self.data = np.array(l)
        
        return self.data
    
    def OutRes(self):
        out = open(self.OutName,'w')
        for i in self.lLabel:
            print >> out,"%f" %(i)
            
        out.close()
        
        
    def Process(self):
        self.LoadData()
        self.lLabel = self.ProcessData(self.data)
        self.OutRes()
        return True
    
    
    def ProcessData(self,data):
        model = KMeans(n_clusters=self.k)
        lLabel = model.fit_predict(data)
        lLabel = list(lLabel)
        return lLabel
        
