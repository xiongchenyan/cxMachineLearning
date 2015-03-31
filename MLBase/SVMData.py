'''
Created on Mar 27, 2015 3:40:40 PM
@author: cx

what I do:
Some how store svm data and make out various lines
should be a very lightly used structure
what's my input:

what's my output:


'''
import logging
import json
class SVMDataC(object):
    
    def __init__(self,line = ""):
        self.Init()
        if "" != line:
            self.loads(line)
            
            
    def Init(self):
        self.hFeature = {}
        self.Label = 0
        self.qid = ""
        self.Note = ""
        
    def loads(self,line):
        vCol = line.split('#')
        if len(vCol) > 1:
            self.Note = vCol[-1].strip()
            
        data = vCol[0].strip()
        
        lDataCol = data.split(' ')
        self.Label = float(lDataCol[0])
        if len(lDataCol) < 2:
            return
        lFCol = []
        if lDataCol[1].startswith('qid:'):
            self.qid = lDataCol[1].replace('qid:','')
            lFCol = lDataCol[2:]
        else:
            lFCol = lDataCol[1:]
        logging.debug('get feature col %s',json.dumps(lFCol))    
        for fcol in lFCol:
            dim,score = fcol.split(':')
            score = float(score)
            self.hFeature[dim] = score
            
        return True
    
    
    def dumps(self):
        res = "%s" %(self.Label)
        if self.qid != "":
            res += ' qid:%s' %(self.qid)
        lFeature = self.hFeature.items()
        lFeature.sort(key=lambda item: int(item[0]))
        
        res += ' '.join([item[0] + ":" + item[1] for item in lFeature ])
        
        if "" != self.Note:
            res += ' # %s' %(self.Note)
            
        return res
    
    
    def DumpMtxLine(self):
        res = '%s,' %(self.Label)
        lFeature = self.hFeature.items()
        lFeature.sort(key=lambda item: int(item[0]))
        
        res += ','.join([item[1] for item in lFeature ])
        
        if "" != self.qid:
            res += ',%s' %(self.qid)
            
        return res
    
    
    @staticmethod
    def TransferSVMDataToMtx(InName,OutName):
        out = open(OutName,'w')
        
        for line in open(InName):
            data = SVMDataC(line.strip())
            print >>out, data.DumpMtxLine()
            
        out.close()
        logging.info('svm data [%s] to mtx [%s]',InName,OutName)
        
        return True
        
        
        
        
if __name__ == '__main__':
    import sys
    '''
    going to have more transfer format stuff
    '''
    logging.basicConfig(level=logging.DEBUG)
    if 3 != len(sys.argv):
        print "transfer svm data to mtx"
        print "2 para: input + output"
        sys.exit()
        
        
    SVMDataC.TransferSVMDataToMtx(sys.argv[1], sys.argv[2])        
        
        
            
    
        