'''
Created on Mar 19, 2015 9:38:13 PM
@author: cx

what I do:
I simply run svm by given parameter format
what's my input:
input parameter(json) prediction_res_name
what's my output:
the predicted result in prediction
Mine is in trec format
'''




import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import subprocess
import logging
import json
class RankSVMTrainAndPreC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.C = 0.001
        self.lModelTrainCmd = ['/bos/usr0/cx/SVMLight/svm_rank_learn','-c']
        self.lModelTestCmd = ['/bos/usr0/cx/SVMLight/svm_rank_classify']
        self.TrainInName = ""
        self.TestInName = ""
        self.PreName = "" 
        
    
    def Train(self):
        lCmd = self.lModelTrainCmd + ['%s' %(self.C),self.TrainInName,self.TrainInName + '_model']
        logging.info('training %s',json.dumps(lCmd))
        OutStr = subprocess.check_output(lCmd)
        logging.info(OutStr)
        return True
    
    
    def Predict(self):
        lCmd = self.lModelTestCmd + [self.TestInName,self.TrainInName + '_model', self.PreName]
        logging.info('testing %s', json.dumps(lCmd))
        OutStr = subprocess.check_output(lCmd)
        logging.info(OutStr)
        return True
    
    
    
    def Process(self,TrainInName,TestInName,ParaStr,PreOutName):
        hPara = json.loads(ParaStr)
        if type(hPara) != dict:
            logging.error('%s not a dict json',ParaStr)
            return False
        
        if not 'c' in hPara:
            logging.error('%s doesn\'t contain c', ParaStr)
            return False
        self.C = float(hPara['c'])        
        self.TrainInName = TrainInName
        self.TestInName = TestInName
        self.PreName = PreOutName
        
        self.Train()
        self.Predict()
        logging.info('rank svm train and test done')
        return True
    
    
if __name__ == '__main__':
    import sys
    if 5 != len(sys.argv):
        print "4 para: train data, test data , para str (json format), out"
        sys.exit()
        
        
    processor = RankSVMTrainAndPreC(sys.argv[1])
    processor.Process(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
        
        
        
