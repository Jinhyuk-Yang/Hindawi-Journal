import random

def randomDM(n):
  count = 0
  string = 'module: example'+str(n)+'\n'
  for i in range(n):
    for j in range(3*count+2):
      string += ' '
    string += ('+--rw '+str(i))
    if random.choice([0, 1]) == 1:
      string += ' string'
    else:
      count += 1
    string += '\n'
  return string.rstrip()

for i in range(20, 1001, 20):
  fo = open('DataModel/dm'+str(i), 'w')
  fo.write(randomDM(i))
  fo.close()
