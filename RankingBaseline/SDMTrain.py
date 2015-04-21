'''
Created on Apr 21, 2015 10:42:03 AM
@author: cx

what I do:
for all queries:
    do sdm
    evaluate
return one score (mean ERR@20)
confs are preloaded
what's my input:
input: query in + para str (near weight_uw weight) 
what's my output:
mean ERR@20

'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.Conf import cxConfC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
from IndriSearch.QueryGenerator import QueryGeneratorC

import sys
import logging



def EvaluatePerQ(qid,query,Searcher,Evaluator):
    lDoc = Searcher.RunQuery(query,qid)
    lDocNo = [Doc.DocNo for Doc in lDoc]
    Measure = Evaluator.EvaluatePerQ(qid,query,lDocNo)
    return Measure

def ReadAndGenerateQuery(InName,NearWeight,UWWeight):
    lLine = open(InName).read().splitlines()
    lQidQuery = [line.split('\t') for line in lLine]
    lQidQuery = [[qid,QueryGeneratorC.GenerateSDM(query,NearWeight,UWWeight)] for qid,query in lQidQuery]
    return lQidQuery



def SegParaStr(ParaStr):
    try:
        ConfInName,NearWeight,UWWeight = ParaStr.split('_')
    except:
        logging.error('para str [%s] format error. format:[confname_nearweight_uwweight]',ParaStr)
        sys.exit()
    NearWeight = float(NearWeight)
    UWWeight = float(UWWeight)
    return ConfInName,NearWeight,UWWeight    
    

if 4 != len(sys.argv):
    print "query in + para str(confname_nearweight_uwweight) + outname"
    sys.exit()

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

ConfInName,NearWeight,UWWeight = SegParaStr(sys.argv[2])
InName = sys.argv[1]
OutName = sys.argv[3]


Searcher = IndriSearchCenterC(ConfInName)
Evaluator = AdhocEvaC(ConfInName)

lQidQuery = ReadAndGenerateQuery(InName, NearWeight, UWWeight)
logging.info('sdm q generated')

lMeasure = [EvaluatePerQ(qid, query, Searcher, Evaluator) for qid,query in lQidQuery]
logging.info('searched and evaluated')
MeanMeasure = AdhocMeasureC.AdhocMeasureMean(lMeasure)


out = open(OutName,'w')
print >> out, '%f' %(MeanMeasure.err)
out.close()
logging.info('sdm train [%s][%s] finished',InName,sys.argv[2])






