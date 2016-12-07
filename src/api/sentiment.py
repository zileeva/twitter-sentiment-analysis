import os
import re
import ast
import sentence_preprocessor, naive_bayes_classifier

import nltk.classify
import nltk.sentiment.util
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
preprocessor = sentence_preprocessor.Preprocessor()
feature_vectors = []
feature_list = []
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

def get_word_feature_vector(sentence):
  f_v = []
  words = sentence.split()
  for word in words:
    if (word not in stopwords):
      word = word.strip('\'"?,.')
      f_v.append(word.lower())
  return f_v

def get_bigram_feature_vector(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]','', text)
    bigramFeatureVector = []
    for item in nltk.bigrams(text.split()):
      bigramFeatureVector.append(item)
    return bigramFeatureVector

def get_negation_feature_vector(sentence):
  f_v = []
  words = sentence.split()
  f_v = preprocessor.mark_negation(words)
  return f_v

def get_emoticon_feature_vector(sentence):
  f_v = []
  words = sentence.split()
  f_v = preprocessor.mark_emoticons(words)
  return f_v

def get_pos_tag_feature_vector(sentence):
  f_v = []
  words = sentence.split()
  f_v = preprocessor.mark_pos_tag(words)
  return f_v

def get_all_f_v(sentence):
  f_v = []
  f_v.append(get_word_feature_vector(sentence))
  f_v.append(get_bigram_feature_vector(sentence))
  f_v.append(get_negation_feature_vector(sentence))
  f_v.append(get_emoticon_feature_vector(sentence))
  f_v.append(get_pos_tag_feature_vector(sentence))
  return f_v

def get_feature_vectors(processed_data):
  feature_data = []
  for sentence in processed_data:
    sentiment = sentence[1]
    feature_vectors = get_all_f_v(sentence[0])
    feature_vectors = [val for sublist in feature_vectors for val in sublist]
    feature_data.append((feature_vectors, sentiment))
  return feature_data

def get_uni_word_features(sentence):
  features = {}
  for f in feature_list:
    features[f] = (f in set(sentence))
  return features

def get_bi_word_features(sentence):
  features = {}
  for f in feature_list:
    features[f] = (f in set(nltk.bigrams(sentence)))
  return features

def get_negation_features(sentence):
  features = {}
  for f in feature_list:
    features[f] = (f in set(preprocessor.mark_negation(sentence)))
  return features

def get_emoticon_features(sentence):
  features = {}
  for f in feature_list:
    features[f] = (f in set(preprocessor.mark_emoticons(sentence)))
  return features

def get_pos_tag_features(sentence):
  features = {}
  for f in feature_list:
    features[f] = (f in set(preprocessor.mark_pos_tag(sentence)))
  return features

def extract_features(featured_sentence):
  features = {}
  features.update(get_uni_word_features(featured_sentence))
  features.update(get_bi_word_features(featured_sentence))
  features.update(get_negation_features(featured_sentence))
  features.update(get_emoticon_features(featured_sentence))
  features.update(get_pos_tag_features(featured_sentence))
  return features

def extract_features_all(featured_sentences):
  features = {}
  features.update(get_uni_word_features(featured_sentences[0]))
  features.update(get_bi_word_features(featured_sentences[1]))
  features.update(get_negation_features(featured_sentences[2]))
  features.update(get_emoticon_features(featured_sentences[3]))
  features.update(get_pos_tag_features(featured_sentences[4]))
  return features

def write_training_data(data):
  file_name = open(os.path.abspath(__file__ + "/../../../dataset") + "/" + "training_featured_data.txt", 'w')
  for item in data:
    file_name.write("%s %s\n" % (item[0], item[1]))

def read_training_data():
    training_data = []
    data = open(os.path.abspath(__file__ + "/../../../dataset") + "/" + "training_featured_data.txt")
    for sentence in data:
      sentiment = sentence[-2:].rstrip()
      training_data.append((ast.literal_eval(sentence[:-2]), sentiment))
    return training_data

def classify(data):
  training_data = nltk.classify.util.apply_features(extract_features, data)
  write_training_data(training_data)
  print training_data
  training_data = read_training_data()
  classifier = nltk.NaiveBayesClassifier.train(training_data)

  testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis excellent sound how, not really impressed :('
  processedTestTweet = preprocessor.preprocess(testTweet)
  sentiment = classifier.classify(extract_features_all(get_all_f_v(processedTestTweet)))
  print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)


if __name__ == "__main__":

  sample_data = get_sample_data([ 'positives.txt', 'negatives.txt'])
  processed_data = preprocess(sample_data)
  feature_vectors = get_feature_vectors(processed_data)
  feature_list = [f[0] for f in feature_vectors]
  feature_list = [val for sublist in feature_list for val in sublist]
  classify(feature_vectors)

