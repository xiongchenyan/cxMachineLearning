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

class CVTrainJobSubmitterC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.workdir = ""
        self.lCmd = []
        self.lParaStr = []
        self.DataInName = ""
        self.K = 5
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "in\nworkdir\nparafile\ncmd\nk"
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.workdir = self.conf.GetConf('workdir')
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)
        self.lCmd = self.conf.GetConf('cmd')
        if type(self.lCmd) != list:
            self.lCmd = [self.lCmd]
        
        ParaInName = self.conf.GetConf('parafile')
        self.lParaStr = open(ParaInName).read().splitlines()
        
        self.DataInName = self.conf.GetConf('in')
        
        self.K = int(self.conf.GetConf('k', self.K))
        
        logging.info('conf all loaded')
        
    
    def CreateFolds(self):
        '''
        create folds
        '''   
        lTrainFile = []
        lTestFile = []
        for i in range(self.K):
            lTrainFile.append(open(self.workdir + '/train_%d'%(i),'w'))
            lTestFile.append(open(self.workdir + '/test_%d'%(i),'w'))
        
        cnt = 0
        for line in open(self.DataInName):
            line = line.strip()
            for i in range(self.K):
                if i == (cnt % self.K):
                    print >> lTestFile[i], line
                else:
                    print >> lTrainFile[i], line            
            cnt += 1
            
        logging.info('create train test folds done')
        
        return True
    
    def Submit(self):
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
    
    
    def Process(self):
        logging.info('start working on training cv folds')
        self.CreateFolds()
        logging.info('start submitting jobs for all folds \times parameters')
        self.Submit()
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
        
        
            
                             
                             
        
         
    
        
