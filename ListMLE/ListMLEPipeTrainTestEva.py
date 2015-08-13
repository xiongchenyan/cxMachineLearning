'''
Created on Aug 12, 2015 7:14:48 PM
@author: cx

what I do:
    I train test and evaluate ListMLE
what's my input:
    query-doc features
    train q
    test q
    qrel for evaluation
what's my output:
    evaluation result

'''




import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
import logging
from cxBase.Conf import cxConfC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
from ListMLETrain import ListMLETrainC,ListMLEDocC

from HCCRF.HCCRFBase import HCCRFBaseC

class ListMLEPipeTrainTestEvaC(object):
    
    def __init__(self):
        self.Init()
        
        
    def Init(self):
        self.Evaluator = AdhocEvaC()
        self.Evaluator.Prepare()
        self.DataDir = '/bos/usr0/cx/tmp/GraphRepresentation/GraphFeature/CW09GraphFeatures/Feature/'
        
        self.Learner = ListMLETrainC()
        
    
    
    def FormListMLEDoc(self,GraphData):
        DocData = ListMLEDocC()
        DocData.X = GraphData.NodeMtx[0,:]
        DocData.DocNo = GraphData.DocNo
        DocData.rel = GraphData.rel
        return DocData
    
    
    def ReadTargetQDocData(self,QIn,DataDir):
        llGraphData = HCCRFBaseC.ReadTargetGraphData(QIn,DataDir)
        
        llQDocData= [ [self.FormListMLEDoc(GraphData) for GraphData in lGraphData] for lGraphData in llGraphData]
        return llQDocData
    
    
            
        
    def Process(self,TrainQueryIn,TestQueryIn,ParaStr, EvaOutName):
        logging.info('training using [%s] testing using [%s] eva out to [%s]',TrainQueryIn,TestQueryIn,EvaOutName)
        
        
        conf = cxConfC()
        conf.ParseParaStr(ParaStr)
        
        self.DataDir = conf.GetConf('datadir',self.DataDir)
        
        logging.info('pipe start training')
        
        
        llTrainQDocData = self.ReadTargetQDocData(TrainQueryIn,self.DataDir)
        llTestQDocData = self.ReadTargetQDocData(TestQueryIn,self.DataDir)
        
        
        
        w = self.Learner.Train(llTrainQDocData)
        
        
        logging.info('pipe start testing')
        
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
        
        out = open(EvaOutName,'w')
        for qid,EvaRes in zip(lQid,lEvaRes):
            print >>out, qid + '\t' + EvaRes.dumps()
            
        out.close()
        logging.info('finished, eva res [%s]',lEvaRes[-1].dumps())
        return True
    
    

if __name__ == '__main__':
    import sys
    if 5 != len(sys.argv):
        print "4 para: train q, test q , para str, out"
        print 'parastr: datadir='
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       

        
    Processor = ListMLEPipeTrainTestEvaC()
    Processor.Process(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4])    
            
        
        
        
        
     
    
    
    
        
