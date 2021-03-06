'''
Created on my MAC May 28, 2015-6:10:24 PM
What I do:
analysis the power of each feature
    in SVM format
What's my input:
SVM data
qrel file for evaluation
What's my output:
the mean map,ndcg,err of each feature when ranking alone
and random result (random expectation)
@author: chenyanxiong
'''


import site
from LeToR.LeToRFeatureFilter import lLeToRData
from IndriRelate.IndriQueryParameterRun import qid


site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from AdhocEva.AdhocEva import AdhocEvaC
from LeToR.LeToRDataBase import LeToRDataBaseC
import logging
import random

class LeToRFeatureAnalysisC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Evaluator = AdhocEvaC()
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.Evaluator.SetConf(ConfIn)
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        AdhocEvaC.ShowConf()
        
    def FormRankByOneFeature(self,llLeToRData,FeatureId):
        '''
        lLeToRData is the svm format data for a query
        rank by this fid
        return lDocNo for this qid
        '''
        FeatureId = int(FeatureId)
        llDocNo = []
        for lLeToRData in llLeToRData:
            lDocNoScore = []
            for LTRData in lLeToRData:
                score = 0
                if FeatureId in LTRData.hFeature:
                    score = LTRData.hFeature[FeatureId]
                lDocNoScore.append([LTRData.DocNo,score])
            lDocNoScore.sort(key=lambda item:item[1], reverse = True)
            llDocNo.append([item[0] for item in lDocNoScore])
            
            
        
        return llDocNo
    
    def FormRandomExpectRank(self,llLeToRData):
        
        llDocNo = []
        for lLeToRData in llLeToRData:
            lDocNo = [data.DocNo for data in lLeToRData]
            random.shuffle(lDocNo)
            llDocNo.append(lDocNo)
        
        return llDocNo
            
            
            
            
            
        
    
    def PipeRun(self,SVMDataInName,OutName):
        lLines = open(SVMDataInName).read().splitlines()
        
        lLeToRData = [LeToRDataBaseC(line) for line in lLines]
        llLeToRData = LeToRDataBaseC.SliceViaQid(lLeToRData)
        lQid = [l[0].qid for l in llLeToRData]
        
        
        hFeature = {}
        for ltr in lLeToRData:
            hFeature.update(ltr.hFeature)
            
        lFid = hFeature.keys()
        lFid = [int(Fid) for Fid in lFid]
        
        lFid.sort()
        
        out = open(OutName,'w')
        
        for FeatureId in lFid:
            llDocNo = self.FormRankByOneFeature(llLeToRData, FeatureId)
            EvaRes = self.Evaluator.EvaluateMul(lQid, [], llDocNo)
            print >>out, '%s\t%s' %(FeatureId,EvaRes.dumps())
            logging.info('feature [%d] evaluated',FeatureId)
        
        llRandDocNo = self.FormRandomExpectRank(llLeToRData)
        RandEvaRes = self.Evaluator.EvaluateMul(lQid, [], llRandDocNo)
        print >>out, 'rand\t%s' %(RandEvaRes.dumps())
        logging.info('random result evaluated')
        out.close()
        logging.info('finished')
        return
        
        
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I evaluate each feature in SVM LTR data by its performance alone'
        print 'conf'
        LeToRFeatureAnalysisC.ShowConf()
        print 'in\nout'
        sys.exit()
        
    Analysisor = LeToRFeatureAnalysisC(sys.argv[1])
    conf = cxConfC(sys.argv[1])
    SVMDataInName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    
    Analysisor.PipeRun(SVMDataInName, OutName)

        
        
        
        
        
        
