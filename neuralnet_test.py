from random import *
import numpy as np
import time
import sys

n = int(sys.argv[1])
m = int(sys.argv[2])

nsf_capability = []
capabilitylist = []
learning_input = []
learning_output = []
test_input = []
unique = randint(0, n-1)
for i in range(n):
  capabilitylist.append(str(i))
  if i == unique:  test_input.append(True)
  elif randint(0, 1) == 1:  test_input.append(True)
  else:  test_input.append(False)
for i in range(n, m):
  capabilitylist.append(str(i))
  if randint(0, 1) == 1:  test_input.append(True)
  else:  test_input.append(False)

for i in range(n):
  learning_output.append([])
  nsf_temp = [str(i)]
  for j in range(10):
    selected = randint(n, m-1)
    if not (str(selected) in nsf_temp):
      nsf_temp.append(str(selected))
  nsf_capability.append(nsf_temp)

#print(nsf_capability)
#print(test_input)

learning_temp = []
for i in range(len(capabilitylist)):
    learning_temp.append(False)
learning_input.append(learning_temp)
for i in range(len(nsf_capability)):
    learning_output[i].append(False)


for x in range(len(nsf_capability)):
    learning_temp = []
    for i in range(len(capabilitylist)):
        if capabilitylist[i] in nsf_capability[x]:
            learning_temp.append(True)
        else:
            learning_temp.append(False)
    learning_input.append(learning_temp)
    for y in range(len(nsf_capability)):
        learning_output[y].append(x==y)

for i in range(len(nsf_capability)):
    capa_temp = []
    for j in range(len(nsf_capability[i])):
        capa_temp.append(nsf_capability[i][j])
    for j in range(len(nsf_capability)):
        if i!=j:
            for k in range(len(nsf_capability[j])):
                if nsf_capability[j][k] in capa_temp:
                    capa_temp.remove(nsf_capability[j][k])
    learning_temp = []
    #print(capa_temp)
    for j in range(len(capabilitylist)):
        if capabilitylist[j] in capa_temp:
            learning_temp.append(True)
        else:
            learning_temp.append(False)
    learning_input.append(learning_temp)
    for y in range(len(nsf_capability)):
        learning_output[y].append((i==y and len(capa_temp)>0))

learningrate = 0.05
inputsize = m
hiddensize = m+n
outputsize = n
error = 0.0

# target data cases setting for learning
numberofcase = len(learning_input)
inputcaselist = learning_input
targetcaselist = []
for i in range(numberofcase):
	targettemp = []
	for j in range(n):
		if learning_output[j][i] == True:  targettemp.append(1)
		else:  targettemp.append(0)
	targetcaselist.append(targettemp)



# sigmoid function for value decision
def sigmoid(x):
	return 1 / (1 + np.exp((-1)*round(x, 10)))

# perceptron declaring
class Perceptron:
	def setWeight(self, weights):
		self.weight = weights
		self.size = len(self.weight)

	def loadWeight(self, infofile):
		fi = open(infofile, 'r')
		self.size = int(fi.readline())
		self.weight = []
		for i in range(self.size):
			self.weight.append(float(fi.readline()))
		fi.close()

	def storeWeight(self, infofile):
		fo = open(infofile, 'w')
		fo.write("%d\n" % self.size)
		for i in range(self.size):
			fo.write("%f\n" % self.weight[i])
		fo.close()

	def forwarding(self, inputs):
		output = 0.0
		for i in range(0, self.size):
			output += self.weight[i] * inputs[i]
		return sigmoid(output)

	def __init__(self, n):
		self.size = n
		self.weight = []
		# print(self.size)
		for i in range(0, n):
			self.weight.append(uniform(0.0, 1.0)-0.5)
			# print(self.weight[i])

starttime = time.time()
# perceptrons setting for Neural Network
hiddenlayer = []
outputlayer = []
for i in range(hiddensize):
	per = Perceptron(inputsize)
	hiddenlayer.append(per)
	
for i in range(outputsize):
	per = Perceptron(hiddensize)
	outputlayer.append(per)

# forward function
def forward(inputs):
	global hiddensize
	global outputsize
	global hiddenlayer
	global outputlayer
	hiddenvaluelist = []
	outputvaluelist = []
	for i in range(hiddensize):
		hiddenvaluelist.append(hiddenlayer[i].forwarding(inputs))
	for i in range(outputsize):
		outputvaluelist.append(outputlayer[i].forwarding(hiddenvaluelist))
	return outputvaluelist

def onestepLearning():
	global learningrate
	global inputsize
	global hiddensize
	global outputsize
	global hiddenlayer
	global outputlayer
	global inputcaselist
	global targetcaselist
	global numberofcase
	outputcaselist = []
	hiddencaselist = []

	for i in range(numberofcase):
		hiddenvaluelist = []
		for j in range(hiddensize):
			hiddenvaluelist.append(hiddenlayer[j].forwarding(inputcaselist[i]))
		hiddencaselist.append(hiddenvaluelist)
	for i in range(numberofcase):
		outputvaluelist = []
		for j in range(outputsize):
			outputvaluelist.append(outputlayer[j].forwarding(hiddencaselist[i]))
		outputcaselist.append(outputvaluelist)

	for j in range(hiddensize):
		for k in range(outputsize):
			weightincrease = 0.0
			for n in range(numberofcase):
				weightincrease += ( (targetcaselist[n][k]-outputcaselist[n][k])*outputcaselist[n][k]*(1-outputcaselist[n][k])*hiddencaselist[n][j] )
			weightincrease *= learningrate
			#print(weightincrease)
			outputlayer[k].weight[j] += weightincrease

	for j in range(hiddensize):
		for i in range(inputsize):
			weightincrease = 0.0			
			for n in range(numberofcase):
				temp = 0.0
				for k in range(outputsize):
					temp += ( outputlayer[k].weight[j]*(targetcaselist[n][k]-outputcaselist[n][k])*outputcaselist[n][k]*(1-outputcaselist[n][k]) )
				temp *= ( inputcaselist[n][i]*hiddencaselist[n][j]*(1-hiddencaselist[n][j]) )
				weightincrease += temp
			weightincrease *= learningrate
			#print(weightincrease)
			hiddenlayer[j].weight[i] += weightincrease

def calculateError():
	global numberofcase
	global inputcaselist
	global targetcaselist
	error = 0.0
	outputcaselist = []
	for i in range(numberofcase):
		outputcaselist.append(forward(inputcaselist[i]))
	for n in range(numberofcase):
		for k in range(outputsize):
			error += ( (targetcaselist[n][k] - outputcaselist[n][k]) * (targetcaselist[n][k] - outputcaselist[n][k]) ) * 0.5
	return error


		
# machine learning (FNN)

errortemp = 10000000000.0
while True:
	onestepLearning()
	#print(calculateError())
	newerror = calculateError()
	if errortemp - newerror < 0.01:
		break
	errortemp = newerror

print(calculateError())

#end time
endtime = time.time()
print (endtime-starttime)

# DT provisioning time
start_time = time.time()
count = 0
test_output = forward(test_input)
for i in range(n):
	if test_output[i] < 0.5:	test_output[i] = False
	else:	test_output[i] = True
	if test_output[i] == (test_input[i]):	count += 1
print("DNN Provisioning Time: %s seconds"%(time.time() - start_time))
print("DNN Accuracy : "+str((float(count)/n)*100))

