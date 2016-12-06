import os
import re
import sentence_preprocessor, naive_bayes_classifier

import nltk.classify
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
preprocessor = sentence_preprocessor.Preprocessor()

def get_data(list_of_files):
  data = []
  for file_name in list_of_files:
    raw_data = open(os.path.abspath(__file__ + "/../../../dataset") + "/" + file_name)
    for sentence in raw_data:
      sentiment = sentence[-2:].rstrip()
      data.append((sentence[:-2], sentiment))
  return data


def preprocess(sample_data):
  preprocessed = []
  for sentence in sample_data:
    preprocessed.append(preprocessor.preprocess_tuple(sentence))
  return preprocessed

def get_feature_vector(sentence):
  f_v = []
  words = sentence.split()
  for word in words:
    if (word not in stopwords):
      word = word.strip('\'"?,.')
      f_v.append(word.lower())
  return f_v

feature_list = []
def get_feature_vectors(processed_data):
  feature_data = []
  for sentence in processed_data:
    sentiment = sentence[1]
    feature_vector = get_feature_vector(sentence[0])
    feature_list.extend(feature_vector)
    feature_data.append((feature_vector, sentiment))
  return feature_data

def get_features(sentence):
    sentence_set = set(sentence)
    features = {}
    for f in feature_list:
      features[f.decode("utf8")] = (f in sentence_set)
    return features

def test(data):
  test_data = nltk.classify.util.apply_features(get_features, data)
  classifier = nltk.NaiveBayesClassifier.train(test_data)

  real_sentiments = []
  for s, r in data:
    real_sentiments.append(r)

  print real_sentiments

  test_sentiments = []
  for s, r in data:
    processed_tweet = preprocessor.preprocess(s)
    test_sentiments.append(classifier.classify(get_features(get_feature_vector(processed_tweet))))

  print test_sentiments

def classify(data):
  # c = naive_bayes_classifier.NaiveBayes(data)
  training_data = nltk.classify.util.apply_features(get_features, data)
  classifier = nltk.NaiveBayesClassifier.train(training_data)

# Test function test.classifier 
# Instead of one sentence, have several sentences .. for each sentence preprocess, classify, produce arry of sentiments. 
# sample 
  testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis'
  processedTestTweet = preprocessor.preprocess(testTweet)
  sentiment = classifier.classify(get_features(get_feature_vector(processedTestTweet)))
  # print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)


if __name__ == "__main__":
  sample_data = get_data([ 'test.txt' ]) # 'positives.txt', 'negatives.txt'])
  # print sample_data
  processed_data = preprocess(sample_data)
  # print processed_data
  feature_vectors = get_feature_vectors(processed_data)
  # print feature_vectors
  classify(feature_vectors)
  test(sample_data)
  



