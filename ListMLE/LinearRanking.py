'''
Created on Aug 17, 2015 4:39:12 PM
@author: cx

what I do:
    Rank via Linear ranking
what's my input:
    data, read by ListMLEPipeTrainTestEvaC
    weights
what's my output:
    ranking and eva res, in output dir


'''

import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import numpy as np
from ListMLE.ListMLEPipeTrainTestEva import ListMLEPipeTrainTestEvaC
from ListMLETrain import ListMLEDocC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
import logging
class LinearRankingC(object):
    
    def __init__(self):
        self.Init()
        
        
    def Init(self):
        self.Evaluator = AdhocEvaC()
        self.Evaluator.Prepare()
        self.DataDir = '/bos/usr0/cx/tmp/GraphRepresentation/GraphFeature/CW09GraphFeatures/EsdRankFeature/'
        
    def ReadPara(self,ParaIn):
        lLines = open(ParaIn).read().splitlines()
        lPara = lLines[0].split()
        return np.array(lPara)
        
            
    
    def PipeRanking(self,TestQueryIn,ParaIn,OutName):
        llTestQDocData = ListMLEPipeTrainTestEvaC.ReadTargetQDocData(TestQueryIn,self.DataDir)
        w = self.ReadPara(ParaIn)
        
        
        lQid = [line.split('\t')[0] for line in open(TestQueryIn).read().splitlines()]
#         llDocScore = [ [ [data.DocNo, data.X.dot(w)] for data in lTestQDocData] for lTestQDocData in llTestQDocData]
        
        llDocScore = []
        for lTestQDocData in llTestQDocData:
            lDocScore = []
            for data in lTestQDocData:
                print 'w: %s' %(np.array2string(w))
                print data.DocNo
                print np.array2string(data.X)
                lDocScore.append([data.DocNo,data.X.dot(w)])
            llDocScore.append(lDocScore)
        
        logging.info('pipe start evaluating')
        
        lEvaRes = []
        
        for qid,lDocScore in zip(lQid,llDocScore):
            lDocScore.sort(key=lambda item:item[1],reverse = True)
            lDocNo = [item[0] for item in lDocScore]
            EvaRes = self.Evaluator.EvaluatePerQ(qid, "", lDocNo)
            lEvaRes.append(EvaRes)
            
        MeanEvaRes = AdhocMeasureC.AdhocMeasureMean(lEvaRes)
        lEvaRes.append(MeanEvaRes)
        lQid.append('mean')
        
        out = open(OutName,'w')
        for qid,EvaRes in zip(lQid,lEvaRes):
            print >>out, qid + '\t' + EvaRes.dumps()
            
        out.close()
        logging.info('finished, eva res [%s]',lEvaRes[-1].dumps())
        return True
    
    
    def RankingForCVFolds(self,TestQPre,ParaPre,OutPre,K=10):
        
        for i in range(K):
            TestIn = TestQPre + '_%d' %(i)
            ParaIn = ParaPre + '_%d' %(i)
            OutName = OutPre + '_%d' %(i)
            self.PipeRanking(TestIn, ParaIn, OutName)
            logging.info('fold [%d] done',i)
        return
        

    
    
    

if __name__ == '__main__':
    import sys
    if 5 != len(sys.argv):
        print "4 para: test pre, para pre, out, k"
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       

        
    Processor = LinearRankingC()
    Processor.RankingForCVFolds(sys.argv[1],sys.argv[2],sys.argv[3], int(sys.argv[4]))    
            
        
        
        
        


