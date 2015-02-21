'''
Created on my MAC Nov 29, 2014-6:15:59 PM
What I do:
I generate svm format data from DataDir
read features from each qid's sub dir
transfer it to SVM format,
    add docno in the end as comment, read from qid_DocNo,
    add score from qid_label
What's my input:
DataDir
What's my output:
SVM format data, to be used by SVMRank
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')

import os,ntpath
from LeToR.LeToRDataBase import LeToRDataBaseC
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from cxBase.WalkDirectory import WalkDir
class GenerateSVMFromDataDirC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.DataDir = ""
        self.OutName = ""
        self.MaxQid = 300
        self.DocNoSuf = "_doc_docNo"
        self.LabelSuf = "_label"
        self.QidRange = "1-200"
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DataDir = self.conf.GetConf('datadir')
        self.OutName = self.conf.GetConf('out')
        self.QidRange = self.conf.GetConf('qidrange',self.QidRange)
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'datadir\nout\nqidrange'
        
        
        
    def TransferOneQ(self,qid):
        FeatureDir = self.DataDir + '/%d/' %(qid)
        if not os.path.exists(FeatureDir):
            print '[%s] dir not exist' %(FeatureDir)
            return []
        lFName = WalkDir(FeatureDir)
        lDocNo = open(self.DataDir + '%d%s' %(qid,self.DocNoSuf)).read().splitlines()
        lLabel = open(self.DataDir + '%d%s' %(qid,self.LabelSuf)).read().splitlines()
        
        lData = []
        for fname in lFName:
            LeToRData = LeToRDataBaseC()
            DocP = ntpath.basename(fname)
            try:
                DocP = int(DocP) - 1
            except ValueError:
                continue
            label = lLabel[DocP]
            DocNo = lDocNo[DocP]
            lLines = open(fname).read().splitlines()
            FeatureStr = lLines[0]
            LeToRData.DocNo = DocNo
            LeToRData.score = float(label)
            LeToRData.qid = str(qid)
            lFValue = [float(item) for item in FeatureStr.split(',')]
            LeToRData.hFeature = dict(zip(range(1,len(lFValue) + 1),lFValue))
            lData.append(LeToRData)
        lData = LeToRDataBaseC.MaxMinNormalize(lData)
        lOutLine = [data.dumps() for data in lData]
        print '[%d] query get [%d] training instance' %(qid,len(lOutLine))
        return lOutLine
    
    
    def Process(self):
        out = open(self.OutName,'w')
        qst,qed = self.QidRange.split('-')
        qst = int(qst)
        qed = int(qed)
        for qid in range(qst,qed + 1):
            lOutLine = self.TransferOneQ(qid)
            print "[%d] get [%d] doc features" %(qid,len(lOutLine))
            if [] == lOutLine:
                continue
            print >>out, '\n'.join(lOutLine)
        out.close()
        print "finished"
        
import sys
if 2 != len(sys.argv):
    GenerateSVMFromDataDirC.ShowConf()
    sys.exit()
    
Processor = GenerateSVMFromDataDirC(sys.argv[1])
Processor.Process()

    
    
            
            
            
            
            