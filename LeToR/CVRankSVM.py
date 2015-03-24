'''
Created on my MAC Nov 29, 2014-10:52:39 PM
What I do:
I am a sub class of CVLeToR, using RankSVM algorithm
What's my input:

What's my output:

@author: chenyanxiong
'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from LeToR.CVLeToR import *
import json
import logging
class CVRankSVMC(CVLeToRC):
    
    def Init(self):
        CVLeToRC.Init(self)
        self.C = 0.001
        self.lModelTrainCmd = ['/bos/usr0/cx/SVMLight/svm_rank_learn','-c']
        self.lModelTestCmd = ['/bos/usr0/cx/SVMLight/svm_rank_classify']
        
    def SetConf(self, ConfIn):
        CVLeToRC.SetConf(self, ConfIn)
        self.C = float(self.conf.GetConf('c', self.C))
        self.lModelTrainCmd.append('%f' %(self.C))
        
    @staticmethod
    def ShowConf():
        CVLeToRC.ShowConf()    
        print 'c'
        
    
    def ReadData(self):
        lLines = open(self.In).read().splitlines()
        self.lData = [LeToRDataBaseC(line) for line in lLines]
        return
    def RunModelForOnePartition(self,k):
        TrainData = self.WorkDir + 'Train_%d' %(k)
        TestData = self.WorkDir + 'Test_%d' %(k)
        ModelData = self.WorkDir + 'Model_%d' %(k)
        PreData = self.WorkDir + 'Pre_%d' %(k)
        
        lTrainCmd = self.lModelTrainCmd + [TrainData,ModelData]
        print "training %s" %(json.dumps(lTrainCmd))
        subprocess.check_output(lTrainCmd)
        
        lTestCmd = self.lModelTestCmd + [TestData,ModelData,PreData]
        
        print "testing %s" %(json.dumps(lTestCmd))
        subprocess.check_output(lTestCmd)
        print "model for [%d] fold done" %(k)
        return
    
    def CollectResult(self):
        #collect result from target positions
        #and fill in self.lQDocRank
        self.lQDocRank = []   #[qid,lDocNoRank]
        hQDocRank = {}
        for k in range(0,self.K):
            PreData = self.WorkDir + 'Pre_%d' %(k)
            TestData = self.WorkDir + 'Test_%d' %(k)
            lData = [LeToRDataBaseC(line) for line in open(TestData).read().splitlines()]
            lScore = [float(line) for line in open(PreData).read().splitlines()]
            for i in range(len(lData)):
                data = lData[i]
                score = lScore[i]
                qid = data.qid
                DocNo = data.DocNo
                if not qid in hQDocRank:
                    hQDocRank[qid] = [[DocNo,score]]
                else:
                    hQDocRank[qid].append([DocNo,score])
                    
                    
        lQDocScore = hQDocRank.items()
        for qid,lDocScore in lQDocScore:
            lDocScore.sort(key=lambda item:item[1],reverse = True)
            lDocRank = [item[0] for item in lDocScore]
            self.lQDocRank.append([qid,lDocRank])
        return
    
        
    def RunWithGivenPara(self,InName,ParaStr,EvaOutName):
        if not self.SetByGivenPara(InName, ParaStr, EvaOutName):
            return
        logging.info('argv set successfully for input [%s]',InName)
        
        self.Process()
        logging.info('process finished, start collectting results')
        
        lLines = open(EvaOutName + '_full_eva').read().splitlines()
        
        MeanErr = float(lLines[-1].split()[-1])
        logging.info('mean err [%f]',MeanErr)
        return MeanErr
        
        
        
        
        
        
        
    def SetByGivenPara(self,InName,ParaStr,EvaOutName):
        self.In = InName
        self.WorkDir = self.In + '_workdir/'
        if not os.path.exists(self.WorkDir):
            os.mkdir(self.WorkDir)
            
        self.OutName = EvaOutName + '_full_eva'
        
        hPara = json.loads(ParaStr)
        if type(hPara) != dict:
            logging.error('para str [%s] no dict type',ParaStr)
            return False
        
        if not 'c' in hPara:
            logging.error('c not in para str [%s]',ParaStr)
            return False
        self.C = float(hPara['c'])
        return True
        
        


if __name__ =='__main__':
    import sys
    if len(sys.argv) == 2:
        processor = CVRankSVMC(sys.argv[1])
        processor.Process()
        logging.info('run by conf done')
        sys.exit()
        
    if len(sys.argv) == 4:
        processor = CVRankSVMC()
        processor.RunWithGivenPara(sys.argv[1], sys.argv[2], sys.argv[3])
        logging.info('run by give para done')
        sys.exit()
        
    print "two ways to run me:"
    print "1 argv: the conf file"
    CVRankSVMC.ShowConf()
    print "3 argv: run by cmds InName, parastr (json format), evaout name (one single score)"
                
            
            
            