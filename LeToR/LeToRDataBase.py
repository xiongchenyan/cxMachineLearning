'''
Created on my MAC Nov 29, 2014-6:27:54 PM
What I do:
I am a simple base class for letor data
What's my input:

What's my output:

@author: chenyanxiong
'''

class LeToRDataBaseC(object):
    def __init__(self,line=""):
        self.Init()
        if line != "":
            self.loads(line)
            
            
    def Init(self):
        self.hFeature = {}
        self.qid = '0'
        self.score = 0
        self.DocNo = ""
        
    def loads(self,line):
        vCol = line.split()
        self.score = float(vCol[0])
        self.qid = vCol[1].replace('qid:','')
        CommentP = vCol.index('#')
        self.DocNo = vCol[CommentP + 1]
        lFeatureStr = vCol[2:CommentP]
        self.hFeature = self.SegFeatureCol(lFeatureStr)
        return
    
    def dumps(self):
        line = "%f qid:%s %s # %s" %(self.score,self.qid,self.MakeFeatureStr(),self.DocNo)
        return line
    
    def HashFeatureName(self,hFeatureName):
        '''
        hashlize feature name
        '''
        if {} == self.hFeature:
            continue
        lName = self.hFeature.keys()
        lName.sort()
        for name in lName:
            if not name in hFeatureName:
                hFeatureName[name] = len(hFeatureName) + 1
        
        hNewFeature = {}
        for key,score in self.hFeature.items():
            KeyId = hFeatureName[key]
            hNewFeature[KeyId] = score
        self.hFeature = hNewFeature
        return hFeatureName
        
            
        
    def SegFeatureCol(self,lFeatureStr):
        hFeature = {}
        for feature in lFeatureStr:
            dim,value = feature.split(':')
            value = float(value)
#             dim =int(dim)
            hFeature[dim] = value
        return hFeature
    
    def MakeFeatureStr(self):
        lDim = self.hFeature.items()
        lDim.sort(key=lambda item:item[0])
        lFeatureStr = ['%s:%f' %(item[0],item[1]) for item in lDim]
        return " ".join(lFeatureStr)
    
    
    @staticmethod
    def MaxFeature(lLeToRData):
        hFeature = {}
        for data in lLeToRData:
            for dim,value in data.hFeature.items():
                score = value
                if dim in hFeature:
                    score = max(value,hFeature[dim])
                hFeature[dim] = score
        return hFeature
    
    @staticmethod
    def MinFeature(lLeToRData):
        hFeature = {}
        for data in lLeToRData:
            for dim,value in data.hFeature.items():
                score = value
                if dim in hFeature:
                    score = min(value,hFeature[dim])
                hFeature[dim] = score
        return hFeature
    
    @staticmethod
    def MaxMinNormalize(lLeToRData):
        hMax = LeToRDataBaseC.MaxFeature(lLeToRData)
        hMin = LeToRDataBaseC.MinFeature(lLeToRData)
        
        for i in range(len(lLeToRData)):
            for dim in lLeToRData[i].hFeature.keys():
                DimMax = hMax[dim]
                DimMin = hMin[dim]
                if DimMax == DimMin:
                    continue
                lLeToRData[i].hFeature[dim] = (lLeToRData[i].hFeature[dim] - DimMin) / (DimMax-DimMin)
        return lLeToRData
        
        
        
        
        
            