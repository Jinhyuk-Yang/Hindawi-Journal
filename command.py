#!/usr/bin/python
#-*- coding:utf-8 -*-

import API.DFAAPI as DFA
import API.CFGAPI as CFG
import API.converter as converter

# construct DFA based Data Extractor
consumer = DFA.dfa_construction('DataModel/cfi_dm.txt')
consumer_dfa = consumer[0]
consumer_extractedinfo = consumer[1]

# construct CFG based Policy Generator
nsf_facing = CFG.cfg_construction('DataModel/nfi_dm.txt')
cfglist = nsf_facing[0]
nsf_requiredinfo = nsf_facing[1]

# construct Data Converter
dataconverter = converter.DataConverter(consumer_extractedinfo, nsf_requiredinfo)

# register NSF by DMS
resttxt = "ingress-action-capa: alert,drop,pass\negress-action-capa: alert,drop,pass\nprocessing: 1000,5000\nBandwidth Outbound: 1000,5000\nBandwidth Inbound: 1000,5000"
dataconverter.registerNSF("nsf-name: general_firewall\nipv4-capa: range-ipv4-address,exact-ipv4-address,ipv4-protocol\ntcp-capa: exact-tcp-port-num,range-tcp-port-num\n"+resttxt)
dataconverter.registerNSF("nsf-name: time_based_firewall\ntime-capabilities: absolute-time,periodic-time\nipv4-capa: range-ipv4-address,exact-ipv4-address,ipv4-protocol\n"+resttxt)
dataconverter.registerNSF("nsf-name: voip_volte_filter\nvoip-volte-capa: voice-id\n"+resttxt)
dataconverter.registerNSF("nsf-name: web_filter\nhttp-capa: url\n"+resttxt)
dataconverter.registerNSF("nsf-name: http_and_https_flood_mitigation\nantiddos-capa: http-flood-action,https-flood-action\n"+resttxt)

# extract data
consumer_extractedlist = DFA.extracting_data('HighLevelPolicy/sns.txt', consumer_dfa, consumer_extractedinfo)

# convert data
dataconverter.inputExtractedData(consumer_extractedlist)
#dataconverter.initializeDB()
dataconverter.convertData()

# policy provisioning
dataconverter.constructDecisionTree()
dataconverter.policyprovisioning(cfglist)

"""
# extract data
dataconsumer_extractedlist = DFA.extracting_data('HighLevelPolicy/voip.txt', consumer_dfa, consumer_extractedinfo)

# convert data
dataconverter.inputExtractedData(consumer_extractedlist)
dataconverter.initializeDB()
dataconverter.convertData()

# policy provisioning
dataconverter.constructDecisionTree()
dataconverter.policyprovisioning(cfglist)

# extract data
dataconsumer_extractedlist = DFA.extracting_data('HighLevelPolicy/ddos.txt', consumer_dfa, consumer_extractedinfo)

# convert data
dataconverter.inputExtractedData(consumer_extractedlist)
dataconverter.initializeDB()
dataconverter.convertData()

# policy provisioning
dataconverter.constructDecisionTree()
dataconverter.policyprovisioning(cfglist)
"""
