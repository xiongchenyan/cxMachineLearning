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
        
    def FormRankByOneFeature(self,lLeToRData,FeatureId):
        '''
        lLeToRData is the svm format data for a query
        rank by this fid
        return lDocNo for this qid
        '''
        FeatureId = int(FeatureId)
        lQidDocNoScore = []
        for LTRData in lLeToRData:
            score = 0
            if FeatureId in LTRData.hFeature:
                score = LTRData.hFeature[FeatureId]
            lQidDocNoScore.append([LTRData.qid, LTRData.DocNo,score])
            
#         lQidDocNoScore.sort(key=lambda item:item[1],reverse = True)
        lQid = []
        llDocNoScore = []
        LastQid = None
        for qid,DocNo,score in lQidDocNoScore:
            if qid != LastQid:
                lQid.append(qid)
                llDocNoScore.append([])
                LastQid = qid
            llDocNoScore[-1].append([DocNo,score])

        llDocNo = []        
        for i in range(len(llDocNoScore)):
            llDocNoScore[i].sort(key=lambda item:item[1], reverse = True)
            llDocNo.append([item[0] for item in llDocNoScore[i]])
        
        return lQid,llDocNo
        
        
    
    def PipeRun(self,SVMDataInName,OutName):
        lLines = open(SVMDataInName).read().splitlines()
        
        lLeToRData = [LeToRDataBaseC(line) for line in lLines]
        
        hFeature = {}
        for ltr in lLeToRData:
            hFeature.update(ltr.hFeature)
            
        lFid = hFeature.keys()
        lFid = [int(Fid) for Fid in lFid]
        
        lFid.sort()
        
        out = open(OutName,'w')
        
        for FeatureId in lFid:
            lQid,llDocNo = self.FormRankByOneFeature(lLeToRData, FeatureId)
            EvaRes = self.Evaluator.EvaluateMul(lQid, [], llDocNo)
            print >>out, '%s\t%s' %(FeatureId,EvaRes.dumps())
            logging.info('feature [%d] evaluated',FeatureId)
        
        out.close()
        logging.info('finished')
        
        
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

        
        
        
        
        
        
