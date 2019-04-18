import numpy as np
import sys
from random import *
import time

"""
capabilitylist = ['outlook', 'temperature', 'humidity', 'wind']
learning_input = [[True, True, True, False], [True, True, True, True], [False, False, True, False], [True, False, True, False], [False, False, False, False], [True, False, False, True], [False, False, True, True]]
learning_output = [False, False, True, False, True, True, False]
generalize_rate = 0.001
test_input = [True, True, False, True]
"""

n = int(sys.argv[1])
m = int(sys.argv[2])
generalize_rate = 0.05

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


def vectorDistance(vector1, vector2):
    result = 0
    for i in range(len(vector1)):
        if vector1[i] != vector2[i]:
            result = result+1
    return result

def kNNalgorithm(db_input, db_output, vector_input, k):
    kth_list_dist = []
    kth_list_output = []
    for i in range(len(db_output)):
        vectordist = vectorDistance(db_input[i], vector_input)
        if len(kth_list_dist) < k:
            kth_list_dist.append(vectordist)
            kth_list_output.append(db_output[i])
            # sort kth-list
            for x in range(0, len(kth_list_dist)):
                for y in range(x+1, len(kth_list_dist)):
                    if kth_list_dist[x] > kth_list_dist[y]:
                        temp_dist = kth_list_dist[x]
                        kth_list_dist[x] = kth_list_dist[y]
                        kth_list_dist[y] = temp_dist
                        temp_output = kth_list_output[x]
                        kth_list_output[x] = kth_list_output[y]
                        kth_list_output[y] = temp_output
        elif vectordist < kth_list_dist[k-1]:
            kth_list_dist.pop()
            kth_list_output.pop()
            kth_list_dist.append(vectordist)
            kth_list_output.append(db_output[i])
            # sort kth-list
            for x in range(0, k):
                for y in range(x+1, k):
                    if kth_list_dist[x] > kth_list_dist[y]:
                        temp_dist = kth_list_dist[x]
                        kth_list_dist[x] = kth_list_dist[y]
                        kth_list_dist[y] = temp_dist
                        temp_output = kth_list_output[x]
                        kth_list_output[x] = kth_list_output[y]
                        kth_list_output[y] = temp_output
            #print(kth_list_dist)

    truecount = 0
    for i in range(k):
        if kth_list_output[i] == True:
            truecount = truecount+1
    falsecount = k-truecount
    if truecount > falsecount:
        #print('kNN Algorithm, k=%d, Result: True' % k)
        return True
    else:
        #print('kNN Algorithm, k=%d, Result: False' % k)
        return False

# declare class for node of decision tree
class DecisionTreeNode:
    # calculate entropy of data list
    def selfEntropy(self):
        learningcount = len(self.learning_output)
        truecount = 0
        for i in range(learningcount):
            if self.learning_output[i] == True:
                truecount += 1
        truerate = float(truecount)/learningcount
        falserate = 1.0 - truerate
        entropy = 0.0
        if truerate != 0.0:
            entropy += (-1)*truerate*np.log2(truerate)
        if falserate != 0.0:
            entropy += (-1)*falserate*np.log2(falserate)
        return [entropy, truerate>=falserate]

    def partition_entropy(self, separator_index):
        # declare variable
        learningcount = len(self.learning_output)
        positivecount = negativecount = 0
        positivelist_input = []
        positivelist_output = []
        negativelist_input = []
        negativelist_output = []
        entropy1 = entropy2 = 0.0

        # divide partition
        for i in range(learningcount):
            if self.learning_input[i][separator_index] == True:
                positivelist_input.append(self.learning_input[i])
                positivelist_output.append(self.learning_output[i])
                positivecount += 1
            else:
                negativelist_input.append(self.learning_input[i])
                negativelist_output.append(self.learning_output[i])
                negativecount += 1

        if positivecount == 0 or negativecount == 0:
            return [1.5, positivelist_input, positivelist_output, negativelist_input, negativelist_output]

        # calculate entropy for partition 1
        truecount = 0
        for i in range(positivecount):
            if positivelist_output[i] == True:
                truecount += 1
        truerate = float(truecount)/positivecount
        falserate = 1.0 - truerate
        if truerate != 0.0:
            entropy1 += (-1)*truerate*np.log2(truerate)
        if falserate != 0.0:
            entropy1 += (-1)*falserate*np.log2(falserate)

        # calculate entropy for partition 2
        truecount = 0
        for i in range(negativecount):
            if negativelist_output[i] == True:
                truecount += 1
        truerate = float(truecount)/negativecount
        falserate = 1.0 - truerate
        if truerate != 0.0:
            entropy2 += (-1)*truerate*np.log2(truerate)
        if falserate != 0.0:
            entropy2 += (-1)*falserate*np.log2(falserate)

        # calculate average of entropy
        positiverate = float(positivecount)/learningcount
        negativerate = 1.0 - positiverate
        average_entropy = positiverate*entropy1+negativerate*entropy2

        # return useful values
        return [average_entropy, positivelist_input, positivelist_output, negativelist_input, negativelist_output]

    # expanding node by recursive method
    def expandNode(self):
        global capabilitylist
        global generalize_rate

        # calculate entropy of data list
        entropylist = self.selfEntropy()

        # if entropy is pretty low: generalization
        if entropylist[0] <= generalize_rate:
            self.isTerminal = True
            self.result = entropylist[1]
        # else: expand tree
        else:
            minentropy = 10.0
            positivelist_input = []
            positivelist_output = []
            negativelist_input = []
            negativelist_output = []
            for i in range(len(capabilitylist)):
                partitioning_result = self.partition_entropy(i)
                if partitioning_result[0] < minentropy:
                    minentropy = partitioning_result[0]
                    positivelist_input = partitioning_result[1]
                    positivelist_output = partitioning_result[2]
                    negativelist_input = partitioning_result[3]
                    negativelist_output = partitioning_result[4]
                    self.separator = capabilitylist[i]
            if len(positivelist_input) == 0 or len(negativelist_input) == 0:
                self.isTerminal = True
                self.result = entropylist[1]
                self.separator = ''
            else:
                self.positive_partition = DecisionTreeNode(positivelist_input, positivelist_output)
                self.negative_partition = DecisionTreeNode(negativelist_input, negativelist_output)

    def __init__(self, learning_input, learning_output):
        self.learning_input = learning_input
        self.learning_output = learning_output
        self.isTerminal = False
        self.separator = ''
        # construct tree
        self.expandNode()

    def running(self, test_input):
        global capabilitylist
        if self.isTerminal == True:
            #print('arrrived to terminal')
            return self.result
        else:
            for i in range(len(capabilitylist)):
                if self.separator == capabilitylist[i]:
                    break
            #print('branch: '+self.separator)
            if test_input[i] == True:
                return self.positive_partition.running(test_input)
            else:
                return self.negative_partition.running(test_input)
"""
decisionTree = DecisionTreeNode(learning_input, learning_output)
test_result = decisionTree.running(test_input)
print(test_result)
"""

#print(capabilitylist)
#print(nsf_capability)



# DT construction time
start_time = time.time()
dtlist = []
for i in range(n):
  dtlist.append(DecisionTreeNode(learning_input, learning_output[i]))
print("DT Construction Time: %s seconds"%(time.time() - start_time))

# DT provisioning time
start_time = time.time()
count = 0
for i in range(n):
  if dtlist[i].running(test_input) == (test_input[i]):  count += 1
print("DT Provisioning Time: %s seconds"%(time.time() - start_time))
print("DT Accuracy : "+str((float(count)/n)*100))

# kNN provisioning time
start_time = time.time()
count = 0
for i in range(n):
  if kNNalgorithm(learning_input, learning_output[i], test_input, 3) == (test_input[i]):  count += 1
print("kNN Provisioning Time: %s seconds"%(time.time() - start_time))
print("kNN Accuracy : "+str((float(count)/n)*100))
