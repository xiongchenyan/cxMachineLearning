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
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')
from LeToR.CVLeToR import *
import json
class CVRankSVMC(CVLeToRC):
    
    def Init(self):
        CVLeToRC.Init(self)
        self.lModelTrainCmd = ['/bos/usr0/cx/SVMLight/svm_rank_learn','-c','0.001']
        self.lModelTestCmd = ['/bos/usr0/cx/SVMLight/svm_rank_classify']
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