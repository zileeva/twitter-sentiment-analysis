import re

class Preprocessor:

  def __init__(self):
    print "Preprocessor initialized"

  def preprocess_tuple(self, tweet):
    sentence = tweet[0]
    sentence = sentence.lower()
    sentence = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',sentence) # convert url
    sentence = re.sub('@[^\s]+','AT_USER',sentence) # convert @
    sentence = re.sub('[\s]+', ' ', sentence) # remove white spaces
    sentence = re.sub(r'#([^\s]+)', r'\1', sentence) # replace hashtags
    sentence = sentence.strip()
    sentence = sentence.rstrip('\'"') # removed quotes
    sentence = sentence.lstrip('\'"')
    return (sentence, tweet[1])

  def preprocess(self, sentence):
    sentence = sentence.lower()
    sentence = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',sentence) # convert url
    sentence = re.sub('@[^\s]+','AT_USER',sentence) # convert @
    sentence = re.sub('[\s]+', ' ', sentence) # remove white spaces
    sentence = re.sub(r'#([^\s]+)', r'\1', sentence) # replace hashtags
    sentence = sentence.strip()
    sentence = sentence.rstrip('\'"') # removed quotes
    sentence = sentence.lstrip('\'"')
    return sentence