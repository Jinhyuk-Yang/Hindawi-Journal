#!/usr/bin/python
#-*- coding:utf-8 -*-

import API.DFAAPI as DFA
import API.CFGAPI as CFG
import time
import random
import sys

def randomDM(n):
  count = 0
  string = 'module: example'+str(n)+'\n'
  for i in range(n):
    for j in range(3*count+2):
      string += ' '
    string += ('+--rw '+str(i))
    if i == n-1:
      string += ' string'
    elif i == 0:
      count += 1
    elif random.choice([0, 1]) == 1:
      string += ' string'
    else:
      count += 1
    string += '\n'
  return string.rstrip()

n = int(sys.argv[1])
fo = open('DataModel/dm'+str(n), 'w')
fo.write(randomDM(n))
fo.close()

# construct DFA based Data Extractor
start_time = time.time()
nsf_test = DFA.dfa_construction('DataModel/dm'+str(n))
nsf_dfa = nsf_test[0]
nsf_extractedinfo = nsf_test[1]
print("DFA Construction Time: %s seconds"%(time.time() - start_time))

# construct CFG based Policy Generator
start_time = time.time()
nsf_facing = CFG.cfg_construction('DataModel/dm'+str(n))
cfglist = nsf_facing[0]
nsf_requiredinfo = nsf_facing[1]
print("CFG Construction Time: %s seconds"%(time.time() - start_time))

nsf_extractedlist = []
for j in range(len(nsf_requiredinfo)):
  nsf_extractedlist.append(['temp'])
print("Policy Size: "+str(len(nsf_requiredinfo)))


start_time = time.time()
fo = open('temp.txt', 'w')
fo.write(CFG.generating_policy(cfglist, nsf_requiredinfo, nsf_extractedlist).rstrip())
fo.close()
print("CFG Parsing Time: %s seconds"%(time.time() - start_time))

start_time = time.time()
nsf_extractedlist = DFA.extracting_data('temp.txt', nsf_dfa, nsf_extractedinfo)
print("DFA Parsing Time: %s seconds"%(time.time() - start_time))


