import csv
import random
import math

class NaiveBayes():

  def __init__(self, dataset):
    print "Initializing Classifier"
    splitRatio = 0.67
    dataset =  [ [6,148,72,35,0,33.6,0.627,50,1], [1,85,66,29,0,26.6,0.351,31,0], [1,85,66,25,0,26.6,0.78,31,0], [8,183,64,7,6,23.3,0.672,32,1], [8,183,64,0,0,23.3,0.672,32,1], [1,89,66,23,94,28.1,0.167,21,0], [0,137,40,35,168,43.1,2.288,33,1], [0,137,40,35,168,43.1,2.288,33,1] ]
    training_set = dataset[:len(dataset) / 2]
    test_set = dataset[len(dataset) / 2 :]
    # print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
    # prepare model
    summaries = self.summarizeByClass(training_set)
    # test model
    predictions = self.getPredictions(summaries, test_set)
    accuracy = self.getAccuracy(test_set, predictions)
    print('Accuracy: {0}%').format(accuracy)
 
  def separateByClass(self, dataset):
    separated = {}
    for i in range(len(dataset)):
      vector = dataset[i]
      if (vector[-1] not in separated):
        separated[vector[-1]] = []
      separated[vector[-1]].append(vector)
    print separated
    return separated
   
  def mean(self, numbers):
    print numbers
    return sum(numbers)/float(len(numbers))
   
  def stdev(self, numbers):
    avg = self.mean(numbers)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(variance)
   
  def summarize(self, dataset):
    print dataset
    summaries = [(self.mean(attribute), self.stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries
 
  def summarizeByClass(self, dataset):
    separated = self.separateByClass(dataset)
    summaries = {}
    for class_value, instances in separated.iteritems():
      summaries[class_value] = self.summarize(instances)
    return summaries
   
  def calculateProbability(self, x, mean, stdev):
    if stdev == 0.0: stdev = 0.1
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
   
  def calculateClassProbabilities(self, summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.iteritems():
      probabilities[classValue] = 1
      for i in range(len(classSummaries)):
        mean, stdev = classSummaries[i]
        x = inputVector[i]
        probabilities[classValue] *= self.calculateProbability(x, mean, stdev)
    return probabilities
        
  def predict(self, summaries, inputVector):
    probabilities = self.calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.iteritems():
      if bestLabel is None or probability > bestProb:
        bestProb = probability
        bestLabel = classValue
    return bestLabel
 
  def getPredictions(self, summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
      result = self.predict(summaries, testSet[i])
      predictions.append(result)
    return predictions
   
  def getAccuracy(self, testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
      if testSet[i][-1] == predictions[i]:
        correct += 1
    return (correct/float(len(testSet))) * 100.0
