'''
Created on Nov 17, 2014 3:04:39 PM
@author: cx

what I do:
I call external SVM (SVMLight) multi class classifier
and pretrained models to classify text
what's my input:
SVM classifier path
SVM pre trained model path
SVM term hash dict (pickle dump of term->id)
text to classify
middirectory to dump data
what's my output:
llScore, the Score of each text belong to classes
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import pickle,json
import random
import subprocess
import os
import shutil
from cxBase.TextBase import TextBaseC
class ExtSVMMultiClassifierC(cxBaseC):
    def Init(self):
        self.SVMClassPath = "/bos/usr0/cx/SVMLight/svm_multiclass_classify"
        self.SVMModel = '/bos/usr0/cx/SVMLight/FbTypeModel'
        self.TempDir = '/bos/usr0/cx/SVMLight/temp/'
        self.TermHashName = "/bos/usr0/cx/SVMLight/FbTypeTermHash"
        self.hTermId = {}
        self.ThisTempName = ""   #the temp name for each file
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.SVMClassPath = self.conf.GetConf('svmpath', self.SVMClassPath)
        self.SVMModel = self.conf.GetConf('svmmodel', self.SVMModel)
        self.TempDir = self.conf.GetConf('tempdir', self.TempDir) + '/'
        if not os.path.exists(self.TempDir):
            print "creating dir [%s]" %(self.TempDir)
            os.makedirs(self.TempDir)
        self.TermHashName = self.conf.GetConf('termhashin',self.TermHashName)
        self.hTermId = pickle.load(open(self.TermHashName))
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "svmpath\nsvmmodel\ntempdir\ntermhashin"
        
        
    def TransferTextToSVMFormat(self,text):
        lTerm = text.split()
        hFeature = {}
        for term in lTerm:
            if not term in self.hTermId:
                continue
            key = self.hTermId[term]
            if not key in hFeature:
                hFeature[key] = 1
            else:
                hFeature[key] += 1
        lFItem = hFeature.items()
        lFItem.sort(key=lambda item:item[0])
        lF = ['%d:%d' %(item[0],item[1]) for item in lFItem]
        res = '1 ' + ' '.join(lF)
        return res
    
    def GenerateTempName(self,lText):
        name = "tmp_%d" %(random.randint(0,10000))
        for text in lText[:30]:
            mid = TextBaseC.DiscardNonAlphaNonDigit(text.replace(' ','').replace('\t',''))
            if len(mid) == 0:
                continue
            name += mid[random.randint(0,len(mid)-1)]
        name = name.replace(' ','')
        self.ThisTempName = self.TempDir + '/' + name
        return self.ThisTempName
    
    def MakeSVMData(self,lText):
        out = open(self.ThisTempName,'w')
        for text in lText:
            print >>out,self.TransferTextToSVMFormat(text)
        out.close()
        
    def Predict(self):
        self.PredictOut=self.ThisTempName + '_pred'
        lCmd = [self.SVMClassPath,self.ThisTempName,self.SVMModel,self.PredictOut]
        print 'svm running: %s' %(json.dumps(lCmd))
        subprocess.check_output(lCmd)
        print "reading predicted output from [%s]" %(self.PredictOut)
        lLines = open(self.PredictOut).readlines()
        lLines = [line.strip() for line in lLines if line.strip() != ""]
        lClass = [line.split()[0] for line in lLines]
        llProb = [[float(weight) for weight in line.split()[1:]] for line in lLines]
        del lLines[:]
        return lClass,llProb
    def Clean(self):
        shutil.rmtree(self.ThisTempName)
        shutil.rmtree(self.PredictOut)
        
        
    def ClassifyData(self,lText):
        self.GenerateTempName(lText)
        self.MakeSVMData(lText)
        lClass,llProb = self.Predict()
#         self.Clean()
        return lClass,llProb
    
        
         
        
    

