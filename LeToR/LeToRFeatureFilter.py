'''
Created on my MAC May 26, 2015-10:55:59 AM
What I do:
quick discard non useful features and do min-max normalizaton
What's my input:

What's my output:

@author: chenyanxiong
'''

from LeToRDataBase import LeToRDataBaseC

import sys

if 3 != len(sys.argv):
    print "svm letor data in + out"
    print "will min-max normalization and discard all same feature dimensions"
    sys.exit()
    
    
lLines = open(sys.argv[1]).read().splitlines()
lLeToRData = [LeToRDataBaseC(line) for line in lLines]

lLeToRData = LeToRDataBaseC.DiscardNonUsefulFeature(lLeToRData)
lLeToRData = LeToRDataBaseC.MaxMinNormalize(lLeToRData)

out = open(sys.argv[2],'w')
for LTRData in lLeToRData:
    print >> out, LTRData.dumps()
    
out.close()
print "finished"
