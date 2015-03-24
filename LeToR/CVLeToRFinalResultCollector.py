'''
Created on Mar 19, 2015 9:39:49 PM
@author: cx

what I do:
I collect the final results get by
CVTrainJobSubmitter
CVTestJobSubmitter
what's my input:
the predict_%d stuff in the work dir   (trec format)
qrel

what's my output:
the evaluation format I used as always
'''


'''
basic flow:
1, read qrel
2, collect doc id and predict score from test_%d and predict_%d
3, evaluate, and output
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
# from SemanticRankEvaluate.SemanticRankEvaluator import *
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
import subprocess
import os
import logging


class CVLeToRFinalResultCollectorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Workdir = ""
        self.K = 5
        self.OutName = ""
        
        self.Evaluator = AdhocEvaC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.Workdir = self.conf.GetConf('workdir')
        self.K = int(self.conf.GetConf('K', 5))
        self.OutName = self.conf.GetConf('out')
        self.Evaluator.SetConf(ConfIn)
        logging.info('CVLeToRFinalResultCollector load conf done')
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "workdir\nK\nout"
        AdhocEvaC.ShowConf()
        
    def LoadQDocRank(self):
        '''
        load qid, doc pair
        load scores
        merge to l = [qid,[doc]] format
        '''
        
        lQidDocRank = []
        for i in range(self.K):
            lQidDocRank.extend(self.LoadOneFoldQDocRank(i))
        
        logging.info('load q doc rank finished')
        
        return lQidDocRank
    
    def LoadOneFoldQDocRank(self,fold):
        lTestLines = open(self.Workdir + '/_test_%d' %(fold)).read().splitlines()
        
        lvCol = [line.split() for line in lTestLines]
        lQidDoc = [[vCol[1].replace('qid:',''),vCol[-1].strip()] for vCol in lvCol]
        
        lScore = open(self.Workdir + '/_predict_%d' %(fold)).read().splitlines()
        lScore = [float(score) for score in lScore]
        
        if len(lQidDoc) != len(lScore):
            logging.error('test and pre file line num not same [%d != %d]',len(lQidDoc),len(lScore))
            return []
        
        
        lQidDocScore = zip(lQidDoc,lScore)
        
        lQidDocRank = []
        for qid,doc,score in lQidDocScore:
            if [] == lQidDocScore:
                lQidDocRank.append([qid,[doc,score]])
                continue
            if qid != lQidDocScore[-1][0]:
                lQidDocRank.append([qid,[doc,score]])
                continue
            lQidDocRank[-1][1].append([doc,score])
            
        for i in range(len(lQidDocRank)):
            l = lQidDocRank[i][1]
            l.sort(key=lambda item:item[1],reverse = True)
            lQidDocRank[i][1] = [item[0] for item in l]
        
        return lQidDocRank
            

    def Evaluate(self,lQidDocRank):
        lPerQEva = []
        for qid,lDocNo in lQidDocRank:
            ThisEva = self.Evaluator.EvaluatePerQ(qid, "", lDocNo)
            lPerQEva.append([qid,ThisEva])

        
        lPerQEva.sort(key=lambda item:int(item[0]))
  
        out = open(self.OutName,'w')
        
        for i in range(len(lPerQEva)):
            print >>out, '%s\t%s'%(lPerQEva[i][0], lPerQEva[i][1].dumps())
        lEvaRes = [item[1] for item in lPerQEva]
        EvaMean = AdhocMeasureC.AdhocMeasureMean(lEvaRes)
        print>>out, 'mean\t' + EvaMean.dumps()
        out.close()
        
        logging.info('evaluate this qid doc set finished')
        logging.info(EvaMean.dumps())
        return True
    
    
    def Process(self):
        logging.info('start load predicted results')
        lQidDocRank = self.LoadQDocRank()
        logging.info('start evaluation')
        self.Evaluate(lQidDocRank)
        logging.info('done')
        return True
    
    
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        CVLeToRFinalResultCollectorC.ShowConf()
        sys.exit()
        
    Collector = CVLeToRFinalResultCollectorC(sys.argv[1])
    Collector.Process()
        
        
            
            
        
        
        
        
    
    
    