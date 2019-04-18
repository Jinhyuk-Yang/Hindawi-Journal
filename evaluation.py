#!/usr/bin/python
#-*- coding:utf-8 -*-

import API.DFAAPI as DFA
import API.CFGAPI as CFG
import API.converter as converter
import threading
import time

n = 50

# construct DFA based Data Extractor
consumer = DFA.dfa_construction('DataModel/cfi_dm.txt')
consumer_dfa = consumer[0]
consumer_extractedinfo = consumer[1]

nsf_test = DFA.dfa_construction('DataModel/nfi_dm.txt')
nsf_dfa = nsf_test[0]
nsf_extractedinfo = nsf_test[1]

# construct CFG based Policy Generator
nsf_facing = CFG.cfg_construction('DataModel/nfi_dm.txt')
cfglist = nsf_facing[0]
nsf_requiredinfo = nsf_facing[1]

# construct Data Converter
dataconverter = converter.DataConverter(consumer_extractedinfo, nsf_requiredinfo)
dataconverter.initializeDB()

policyname = 'sns1'

start_time = time.time()
for i in range(n):
  # extract data
  nsf_extractedlist = DFA.extracting_data('LowLevelPolicy/'+policyname, nsf_dfa, nsf_extractedinfo)
print("Extracting Time: %s seconds"%(time.time() - start_time))

start_time = time.time()
for i in range(n):
  # generate policy  
  CFG.generating_policy(cfglist, nsf_requiredinfo, nsf_extractedlist).rstrip()
print("Generating Time: %s seconds"%(time.time() - start_time))

consumer_extractedlist = DFA.extracting_data('HighLevelPolicy/sns.txt', consumer_dfa, consumer_extractedinfo)
start_time = time.time()
for i in range(n):
  # convert data
  dataconverter.inputExtractedData(consumer_extractedlist)
  dataconverter.convertData()
print("Data Conversion Time: %s seconds"%(time.time() - start_time))

start_time = time.time()
dataconverter.constructDecisionTree()
print("Decision Tree Construction Time: %s seconds"%(time.time() - start_time))

start_time = time.time()
for i in range(n):
  # policy provisioning
  dataconverter.policyprovisioning(cfglist)
print("Policy Provisioning Time: %s seconds"%(time.time() - start_time))
  

