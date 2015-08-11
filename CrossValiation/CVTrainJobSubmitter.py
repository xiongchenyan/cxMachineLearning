'''
Created on Mar 17, 2015 7:18:30 PM
@author: cx

what I do:
I submit jobs for each fold + parameter pair

the job will get the CV results on the fold with given parameter
job must take 3 para: in + para str (json) + out(the evaluation result)


the parameter is packed into a json string



what's my input:
data to split
workdir to dump data
command to call
parameter file, each line is one para to enumerate
what's my output:
submitted jobs

'''


import subprocess

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import json
import logging
import os
from CrossValiation.CVDataPartation import PartitionData, CreateFolds

class CVTrainJobSubmitterC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.workdir = ""
        self.lCmd = []
        self.lParaStr = []
        self.DataInName = ""
        self.K = 5
        self.GroupKeyCol = 1
        self.Spliter = ' '
        self.PreGivenFoldInName = ""
        self.RunType = 'pipe'
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "in\nworkdir\nparafile\ncmd\nk\ngroupkeycol 1\nspliter\nruntype train|pipe\npregivenpartition"
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.workdir = self.conf.GetConf('workdir')
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        self.lCmd = self.conf.GetConf('cmd',self.lCmd)
        
        ParaInName = self.conf.GetConf('parafile')
        self.lParaStr = open(ParaInName).read().splitlines()
        
        self.DataInName = self.conf.GetConf('in')
        
        self.K = int(self.conf.GetConf('k', self.K))
        self.GroupKeyCol = int(self.conf.GetConf('groupkeycol', self.GroupKeyCol))
        
        self.RunType = self.conf.GetConf('runtype', self.RunType)
        
        self.PreGivenFoldInName = self.conf.GetConf('pregivenpartition', self.PreGivenFoldInName)
        
        logging.info('conf all loaded')
        
    
    def MakeFolds(self):
        '''
        create folds
        '''   
        CreateFolds(self.workdir,self.DataInName,self.K,self.GroupKeyCol,self.Spliter,self.PreGivenFoldInName)
               
        return True
    
    def SubmitTrain(self):
        '''
        if multiple parameter, submit training jobs
        '''
        for i in range(self.K):
            for j in range(len(self.lParaStr)):
                ParaStr = self.lParaStr[j]
                ParaStr = ParaStr.replace('"','\\"').replace(' ','')
                lThisCmd = ['qsub'] + self.lCmd + [self.workdir + '/train_%d' %(i), ParaStr,self.workdir + '/res_%d_%d' %(i,j)]
                logging.info('submitting [%s]', ' '.join(lThisCmd))
                OutStr = subprocess.check_output(lThisCmd)
                logging.info(OutStr)
        logging.info('all job submitted')
        return True
    
    def SubmitFullPipe(self):
        '''
        just use first parameter to do train-test
        '''
        for i in range(self.K):
            ParaStr = self.lParaStr[0]
            lThisCmd = ['qsub'] + self.lCmd + [self.workdir+ '/train_%d' %(i),self.workdir + '/test_%d' %(i), ParaStr,self.workdir + '/predict_%d' %(i)]
            logging.info('submitting [%s]', ' '.join(lThisCmd))
            OutStr = subprocess.check_output(lThisCmd)
            logging.info(OutStr)
        logging.info('all pipe job submitted')
        
    
    
    def Process(self):
        logging.info('start working on training cv folds')
        self.MakeFolds()
        if self.RunType == 'train':
            logging.info('start submitting jobs for all folds \times parameters')
            self.SubmitTrain()
        if self.RunType == 'pipe':
            logging.info('start submitting jobs for pipe run')
            self.SubmitFullPipe()
        logging.info('finished')
        return
    
    
if __name__ == '__main__':
    
    import sys
    logging.basicConfig(level=logging.INFO)
    if 2 != len(sys.argv):
        CVTrainJobSubmitterC.ShowConf()
        sys.exit()
        
    Submitter = CVTrainJobSubmitterC(sys.argv[1])
    Submitter.Process()
        
        
            
                             
                             
        
         
    
        
