'''
Created on Mar 19, 2015 8:48:27 PM
@author: cx

what I do:
I collect the best parameters for each fold,
and submit jobs for the test folds

job parameter format:
training data + testing data + parameter(json) + prediction_res_name

what's my input:

same as CVTrainJobSubmitter
But must has res_%d_%d which is the finished results of CVTrain job
larger number means better! (if it is lose or so, the submitted job does the reverse)

what's my output:
the predict_%d_%d results in the workdir

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

class CVTestJobSubmitter(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.workdir = ""
        self.lCmd = []
        self.lParaStr = []
#         self.DataInName = ""
        self.K = 5
        self.lBestPara = []  #the best parameter for each fold (the lines in lParaStr)
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "workdir\nparafile\ncmd\nk"
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.workdir = self.conf.GetConf('workdir') + '/'
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        self.lCmd = self.conf.GetConf('cmd')
        if type(self.lCmd) != list:
            self.lCmd = [self.lCmd]
        
        ParaInName = self.conf.GetConf('parafile')
        self.lParaStr = open(ParaInName).read().splitlines()
        
#         self.DataInName = self.conf.GetConf('in')
        
        self.K = int(self.conf.GetConf('k', self.K))
        
        logging.info('conf all loaded')

    def CollectResultForBestPara(self):
        '''
        collect the results for each fold
        '''
        for i in range(self.K):
            MaxP = -1
            MaxRes = 0
            for j in range(len(self.lParaStr)):
                fname = self.workdir + "/res_%d_%d" %(i,j)
                if not os.path.exists(fname):
                    logging.error('result file [%s] not exists',fname)
                    continue
                
                ThisScore = float(open(fname).read().splitlines()[0])
                if (MaxP == -1) | (MaxRes < ThisScore):
                    MaxRes = ThisScore
                    MaxP = j
            if -1 == MaxP:
                logging.error('fold [%d] no results found', i)
                continue
            logging.info('[%d] fold best para [%d] best train cv res [%f]',i,MaxP,MaxRes)
            self.lBestPara.append(self.lParaStr[MaxP])
        logging.info('best performing parameters collected')
        logging.debug(json.dumps(self.lBestPara))
        return True             
    
    
    def Submit(self):
        if len(self.lBestPara) != self.K:
            logging.error('result not collected/missing')
            return False
        for i in range(self.K):
            ParaStr = self.lBestPara[i].replace('"','\\"').replace(' ','')
            lThisCmd = ['qsub'] + self.lCmd + [self.workdir+ '/train_%d' %(i),self.workdir + '/test_%d' %(i), ParaStr,self.workdir + '/predict_%d' %(i)]
            logging.info('submitting [%s]', ' '.join(lThisCmd))
            OutStr = subprocess.check_output(lThisCmd)
            logging.info(OutStr)
        logging.info('all job submitted')
        return True
    
    
    def Process(self):
        logging.info('start collecting results')
        self.CollectResultForBestPara()
        logging.info('start submitting')
        self.Submit()
        logging.info('done')
        return True
    
    
    
if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) != 2:
        CVTestJobSubmitter.ShowConf()
        logging.error('no config file found')
        sys.exit()
        
    submitter = CVTestJobSubmitter(sys.argv[1])
    submitter.Process()
            
    
    