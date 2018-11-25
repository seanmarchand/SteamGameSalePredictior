import numpy
import matplotlib.pyplot
def predict(features, weights):
  z = numpy.dot(features, weights)
  return 1.0 / (1 + numpy.exp(-z))
#Train our algorithm 
def train(features, labels, weights, alpha, loops):
  #Loop a set amount of times
    for i in range(loops):
      #move closer to the correct weights
      #Gradient descent
        predictions = predict(features, weights)
        gradient = ((numpy.dot(numpy.transpose(features),  predictions - labels))/len(features))*alpha
        weights -= gradient
    return weights
training   = open("trainingData.txt", "r") 
alpha=0.05
loops=10000
features= []
weights=[]
labels=[]
for line in training: 
  thing=line.split(", ")  
  thing[8]="0"
  thing[3] = "0"
  if (int(thing[1])!=0):
    temp = thing[1]
    thing[1] = thing[2]
    thing[2] = temp
    features.append(thing[2:9])
  #If the discount is 0
    if thing[1]!=0:
      labels.append(1)
    else:
      labels.append(0)
#Fill weights with zero to start with
for x in range (0, numpy.shape(features)[1]):
  weights.append(0)
print features
#Convert array into all ints
features2 = [list(map(int, x)) for x in features]
weights=train(features2,labels,weights,alpha,loops)
print weights
