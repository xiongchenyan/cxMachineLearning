'''
Created on Mar 24, 2015 3:25:08 PM
@author: cx

what I do:

what's my input:

what's my output:


'''

import math
import itertools,logging
import json


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


def ReadGivenPartition(GivenPartitionIn):
    lId = []
    if '' != GivenPartitionIn:
        lLines = json.load(open(GivenPartitionIn))
        lId = [int(line) for line in lLines]
    return lId


def PartitionData(lLines,K,GroupKeyCol = -1,Spliter=' ',GivenPartition = ''):
    lData = lLines
    if -1 != GroupKeyCol:
        lData = GroupByKey(lLines,GroupKeyCol,Spliter)
        
    lGivenPartition = ReadGivenPartition(GivenPartition)
    
    
    lTrain = [[] for i in range(K)]
    lTest = [[] for i in range(K)]
    
    
    if [] != lGivenPartition:
        logging.info('partition using given in [%s]',GivenPartition)
        for i in range(len(lData)):
            for j in range(K):
                if (lGivenPartition[i] == j):
                    lTest[j].append(lData[i])
                    logging.debug('[%d] in [%d] test',i,j)
                else:
                    lTrain[j].append(lData[i])        
                    logging.debug('[%d] in [%d] train',i,j)
    else:
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
            
def CreateFolds(workdir,DataInName,K,GroupKeyCol=1,Spliter = '\t',GivenPartitionIn = ''):
    '''
    create folds
    '''   
    logging.info('creating folds')
    lTrainFile = []
    lTestFile = []
    for i in range(K):
        lTrainFile.append(open(workdir + '/train_%d'%(i),'w'))
        lTestFile.append(open(workdir + '/test_%d'%(i),'w'))
    
    
    lLines = open(DataInName).read().splitlines()
    logging.info('total [%d] lines', len(lLines))
    lTrain,lTest = PartitionData(lLines, K, GroupKeyCol, Spliter,GivenPartitionIn)
    logging.info('data partitioned')
    for i in range(K):
        print >> lTrainFile[i], '\n'.join(lTrain[i])
        print >> lTestFile[i], '\n'.join(lTest[i])
        logging.info('train [%d] [%d] line, test [%d] [%d] line',i,len(lTrain[i]),i,len(lTest[i]))
        
    logging.info('create train test folds done')
    
    return True        



