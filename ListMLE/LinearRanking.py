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
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from ListMLE.ListMLEPipeTrainTestEva import ListMLEPipeTrainTestEvaC
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
        
        
    
    def PipeRanking(self,TestQueryIn,ParaIn,OutPre):
        llTestQDocData = ListMLEPipeTrainTestEvaC.ReadTargetQDocData(TestQueryIn,self.DataDir)
        w = self.ReadPara(ParaIn)
        
        lQid = [line.split('\t')[0] for line in open(TestQueryIn).read().splitlines()]
        llDocScore = [ [[data.DocNo, data.X.dot(w)] for data in lTestQDocData] for lTestQDocData in llTestQDocData]
        
        
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
        
        out = open(OutPre,'w')
        for qid,EvaRes in zip(lQid,lEvaRes):
            print >>out, qid + '\t' + EvaRes.dumps()
            
        out.close()
        logging.info('finished, eva res [%s]',lEvaRes[-1].dumps())
        return True
    
    
    def RankingForCVFolds(self,TestQPre,ParaPre,OutFold,K=10):
        
        
        return
        
        
        


