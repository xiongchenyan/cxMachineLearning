'''
Created on Apr 21, 2015 10:57:58 AM
@author: cx

what I do:
for each qid,query
    make sdm q by given para
    run
    write results to output (trec eval format)

what's my input:
null (ignore) + test q in + para(conf_near weight_uw weight) + predict out (trec eval)
what's my output:
trec eval formated doc rankings

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
    

if 5 != len(sys.argv):
    print "null + test query in + para str(confname_nearweight_uwweight) + outname"
    sys.exit()

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

ConfInName,NearWeight,UWWeight = SegParaStr(sys.argv[3])
InName = sys.argv[2]
OutName = sys.argv[4]
out = open(OutName,'w')

Searcher = IndriSearchCenterC(ConfInName)
Evaluator = AdhocEvaC(ConfInName)

lQidQuery = ReadAndGenerateQuery(InName, NearWeight, UWWeight)
logging.info('sdm q generated')

for qid,query in lQidQuery:
    lOutStr = Searcher.RunQueryTrecEvalFormat(query, qid)
    print >>out, '\n'.join(lOutStr)   
logging.info('searched and output')
out.close()
logging.info('sdm test [%s][%s] finished',InName,sys.argv[2])




