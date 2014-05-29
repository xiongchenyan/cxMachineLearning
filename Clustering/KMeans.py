'''
Created on May 29, 2014
call matlab for kmeans
@author: cx
'''
import subprocess
import json
class cxKMeansC(object):
    def Init(self):
        self.k = 8
        self.workdir = ""
        self.DataOut = 'data'
        self.ResOut = 'data'
        self.MFuncName = "/bos/usr0/cx/MatlabCode/cxMatlab/cxKMeans.m"
        
    def __init__(self,workdir="",k=8):
        self.Init()
        self.workdir = workdir
        self.k = k
        
        
    def WriteData(self,data):
        #data is a sparse matrix format [i,j,value]
        out = open(self.workdir + '/' + self.DataOut,'w')
        for triple in data:
            print >>out,"%f,%f,%f" %(triple[0],triple[1],triple[2])
        out.close()
        return
    
    
    def CollectRes(self):
        lLabel = []
        for line in open(self.workdir + '/' + self.ResOut):
            label = int(line.strip(','))
            lLabel.append(label)
        return lLabel
    
    def CallMatlab(self):
        MatlabCommand = ['matlab_7.13', '-nodisplay', '-nodesktop', '-nojvm', '-nosplash', '-r']
        FuncCommand = "%s %s %s %d" %(self.MFuncName,self.workdir + '/' + self.DataOut,
                                   self.workdir + '/' + self.ResOut,self.k)
        MatlabCommand.append(FuncCommand)
        print "calling [%s]" %(json.dumps(MatlabCommand))
        Output = subprocess.check_output(MatlabCommand)
        print "get output [%s]" %(Output)
        
        return
    
    
    def ProcessData(self,data):
        self.WriteData(data)
        self.CallMatlab()
        return self.CollectRes()

