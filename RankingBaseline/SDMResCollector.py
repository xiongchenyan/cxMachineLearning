'''
Created on Apr 21, 2015 11:17:47 AM
@author: cx

what I do:
I collect the predict_0-k result in the CV workdir
combine them to one trec_eval out
evaluate and output
what's my input:
workdir/predict_k
what's my output:
evaluate file

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.Conf import cxConfC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC

import sys
import logging


def CombinePredictRes(workdir,k):
    out = open(workdir +'predict_total','w')
    for i in range(k):
        print >>out, open(workdir + 'predict_%d'%(i)).read().strip()
    out.close()
    logging.info('predict result combined')
    return True


if 2 != len(sys.argv):
    AdhocEvaC.ShowConf()
    print 'workdir\nk\nout'
    sys.exit()
    

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)    
    


    
Evaluator = AdhocEvaC(sys.argv[1])
conf = cxConfC(sys.argv[1])
workdir= conf.GetConf('workdir') + '/'
k = int(conf.GetConf('k'))
OutName = conf.GetConf('out')




CombinePredictRes(workdir, k)
Evaluator.EvaluateTrecOutFile(workdir + 'predict_total', OutName)
logging.info('evaluate result at [%s]',OutName)
        