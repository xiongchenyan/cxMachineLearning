'''
Created on Mar 24, 2015 3:25:08 PM
@author: cx

what I do:

what's my input:

what's my output:


'''

import math
import itertools,logging

def DataSplit(lData,K,NeedDev = False):
    llSplit = []
    lChunks = []
    n = int(math.ceil(float(len(lData)/float(K))))
    for i in xrange(0,len(lData),n):
        lChunks.append(lData[i:i+n])
    for i in range(K):
        lTrain = []
        lTest = []
        lDev = []
        for j in range(len(lChunks)):
            if j == i:
                lTest.extend(lChunks[j])
            else:
                if NeedDev & ((j == len(lChunks) - 1) | ((j == len(lChunks) - 2)& (i==len(lChunks) - 1))):
                    lDev.extend(lChunks[j])
                else:             
                    lTrain.extend(lChunks[j])
        llSplit.append([lTrain,lTest,lDev])

#     print "split res:\n%s"%(json.dumps(llSplit,indent=1))
    return llSplit


def PartitionData(lLines,K,GroupKeyCol = -1,Spliter=' '):
    lData = lLines
    if -1 != GroupKeyCol:
        lData = GroupByKey(lLines,GroupKeyCol,Spliter)
        
    
    lTrain = [[] for i in range(K)]
    lTest = [[] for i in range(K)]
    
    for i in range(len(lData)):
        for j in range(K):
            if (i % K) == j:
                lTest[j].append(lData[i])
                logging.debug('[%d] in [%d] test',i,j)
            else:
                lTrain[j].append(lData[i])        
                logging.debug('[%d] in [%d] train',i,j)
    
    logging.debug('splited')
    
    if -1 != GroupKeyCol:
        lTrain = [list(itertools.chain(*Fold)) for Fold in lTrain]
        lTest = [list(itertools.chain(*Fold)) for Fold in lTest]
        logging.debug('re grouped')
    return lTrain,lTest 


def GroupByKey(lLines,KeyCol,Spliter):
    lData = [[]]
    CurrentKey = ""
    for line in lLines:
        key = line.split(Spliter)[KeyCol]
        if CurrentKey == "":
            CurrentKey = key
            
        if key != CurrentKey:
            lData.append([])
            CurrentKey = key
        lData[-1].append(line)
    logging.debug('[%d] lines grouped into [%d] group',len(lLines),len(lData))
    return lData
            
        



