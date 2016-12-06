import os
import re
import sentence_preprocessor, naive_bayes_classifier

import nltk.classify
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
preprocessor = sentence_preprocessor.Preprocessor()

def get_sample_data(list_of_files):
  sample_data = []
  for file_name in list_of_files:
    data = open(os.path.abspath(__file__ + "/../../../dataset") + "/" + file_name)
    for sentence in data:
      sentiment = sentence[-2:].rstrip()
      sample_data.append((sentence[:-2], sentiment))
  return sample_data


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


def classify(data):
  c = naive_bayes_classifier.NaiveBayes(data)
  # training_data = nltk.classify.util.apply_features(get_features, data)
  # classifier = nltk.NaiveBayesClassifier.train(training_data)

  # testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis'
  # processedTestTweet = preprocessor.preprocess(testTweet)
  # sentiment = classifier.classify(get_features(get_feature_vector(processedTestTweet)))
  # print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)


if __name__ == "__main__":
  sample_data = get_sample_data([ 'test.txt' ]) # 'positives.txt', 'negatives.txt'])
  processed_data = preprocess(sample_data)
  feature_vectors = get_feature_vectors(processed_data)
  # print feature_vectors
  classify(feature_vectors)

