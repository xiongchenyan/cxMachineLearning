'''
Created on May 29, 2014
call matlab for kmeans
@author: cx
'''
import subprocess
import os
import json
class cxKMeansC(object):
    def Init(self):
        self.k = 8
        self.workdir = ""
        self.DataOut = 'data'
        self.ResOut = 'res'
        self.MFuncName = "cxKMeans"
        
    def __init__(self,workdir="",k=8):
        self.Init()
        if "" != workdir:
            self.SetWorkDir(workdir)
        self.SetK(k)
        
    
    def SetWorkDir(self,workdir):
        self.workdir = workdir
        print "kmeans mid dir [%s]" %(self.workdir)
        if not os.path.isdir(self.workdir):
            print "not exist, created"
            os.makedirs(self.workdir)
        
    def SetK(self,k):
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
        MatlabCommand = ['/opt/matlab/7.13/bin/matlab',
                          '-nodisplay', 
                          '-nodesktop',
                           '-nojvm', 
                           '-nosplash',
                           '-singleCompThread',
                            '-r']
        FuncCommand = "\"%s %s %s %d\"" %(self.MFuncName,self.workdir + '/' + self.DataOut,
                                   self.workdir + '/' + self.ResOut,self.k)
        MatlabCommand.append(FuncCommand)
        Command = ' '.join(MatlabCommand)
        print "calling [%s]" %(Command)
#         subprocess.check_output(MatlabCommand)
        os.system(Command)
        return
    
    
    def ProcessData(self,data):
        self.WriteData(data)
        self.CallMatlab()
        return self.CollectRes()

