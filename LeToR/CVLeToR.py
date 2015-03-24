'''
Created on my MAC Nov 29, 2014-9:16:49 PM
What I do:
I partited data and cross validated them using given letor run command,  collect results, and evaluate them.
What's my input:
a file of letor features and labels
a dir for me to dump data
What's my output:
a final evaluation result
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from LeToR.LeToRDataBase import LeToRDataBaseC
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
# from SemanticRankEvaluate.SemanticRankEvaluator import *
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
import subprocess,logging
import os

class CVLeToRC(cxBaseC):
    def Init(self):
        self.In = ""
        self.WorkDir = ""
        self.K = 5
        self.lModelTrainCmd = []
        self.lModelTestCmd = []
        self.Evaluator = AdhocEvaC()
        self.BaseLineEva = ""
        self.OutName = ""
#         self.hQidQuery = {}
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.In = self.conf.GetConf('in')
        self.WorkDir = self.conf.GetConf('workdir') + '/'
        self.BaseLineEva = self.conf.GetConf('baselineeva')
        self.OutName = self.conf.GetConf('out')
#         StemQIn = self.conf.GetConf('queryin')
#         self.hQidQuery = dict([line.split('\t') for line in open(StemQIn).read().splitlines()])
        if not os.path.exists(self.WorkDir):
            os.makedirs(self.WorkDir)
        self.Evaluator.SetConf(ConfIn)
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'in\nworkdir'
        AdhocEvaC.ShowConf()

    def ReadData(self):
        print 'to be implemented in sub classes'
        self.lData = []
        return
    def RunModelForOnePartition(self,k):
        print 'to be implemented in sub classes'
        return
    
    def CollectResult(self):
        #collect result from target positions
        #and fill in self.lQDocRank
        self.lQDocRank = []   #[qid,lDocNoRank]
        print 'to be implemented in sub classes'
        return
        
    def PartitionData(self):
        #could be done in root class.
        lTrain = []
        lTest = []
        FoldSize = int(len(self.lData) / self.K)
        st = 0
        for i in range(self.K):
            ed = st + FoldSize
            lTest = self.lData[st:ed]
            lTrain = self.lData[0:st] + self.lData[ed:]
            lTrainOut = [data.dumps() for data in lTrain]
            lTestOut = [data.dumps() for data in lTest]
            TrainOut = open(self.WorkDir + 'Train_%d' %(i),'w')
            TestOut = open(self.WorkDir + 'Test_%d' %(i),'w')
            print >>TrainOut,'\n'.join(lTrainOut)
            print >>TestOut,'\n'.join(lTestOut)
            TrainOut.close()
            TestOut.close()
            st = ed
        
        return
    

    
    def Evaluate(self):
        lPerQEva = []
        for qid,lDocNo in self.lQDocRank:
#             query = self.hQidQuery[str(qid)]
            ThisEva = self.Evaluator.EvaluatePerQ(qid, "", lDocNo)
            lPerQEva.append([qid,ThisEva])
            
        

        
        lPerQEva.sort(key=lambda item:int(item[0]))
  
        out = open(self.OutName,'w')
        
        lDiffEva = []
        
        for i in range(len(lPerQEva)):
            print >>out, '%s\t%s'%(lPerQEva[i][0], lPerQEva[i][1].dumps())
            
        lEvaRes = [item[1] for item in lPerQEva]
        EvaMean = AdhocMeasureC.AdhocMeasureMean(lEvaRes)
        print>>out, 'mean\t' + EvaMean.dumps()
        out.close()
         
         
        if self.BaseLineEva != "": 
            lBaseEva = AdhocMeasureC.ReadPerQEva(self.BaseLineEva, False)
            lBaseEva = [[str(item[0]),item[1]] for item in lBaseEva]
            lPerQEva = AdhocMeasureC.FillMissEvaByBaseline(lPerQEva, lBaseEva)  
            
            lBaseEva.sort(key=lambda item:int(item[0]))   
            for i in range(len(lPerQEva)):
                lDiffEva.append([lPerQEva[i][0],(lPerQEva[i][1] - lBaseEva[i][1])])                    
            lBaseEvaRes = [item[1] for item in lBaseEva]
            BaseMean = AdhocMeasureC.AdhocMeasureMean(lBaseEvaRes)
            
            lDiffEva.sort(key=lambda item:item[1].ndcg)
            for i in range(len(lDiffEva)):
                print '%s\t%s' %(lDiffEva[i][0],lDiffEva[i][1].dumps())
            
            print 'mean\t' + (EvaMean-BaseMean).dumps()
            print 'mean\t' + (EvaMean).dumps()
         
        
        print 'eva finished'
        return
        
        
    
    def Process(self):
        logging.info('start processing')
        self.ReadData()
        logging.info("Data read")
        self.PartitionData()
        logging.info("partitioned")
        for k in range(0,self.K):
            self.RunModelForOnePartition(k)
            logging.info("fold [%d] train-tested",k)
        self.CollectResult()
        logging.info("result collected")
        self.Evaluate()
        logging.info("evaluated")
        return
    

        
    
    
    