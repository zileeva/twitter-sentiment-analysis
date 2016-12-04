import re, math, collections, itertools
import nltk

def _get_sentences(is_positive):
    if is_positive:
        data = open('../../dataset/positives.txt', 'r')
        pos_or_neg = '1'
    else:
        data = open('../../dataset/negatives.txt', 'r')
        pos_or_neg = '0'

    data_array = []
    # Words with either positive or negative next to them
    for sentence in data:
        if sentence[-2:-1] == pos_or_neg:
            # Remove the 1 or 0 representing positive or negative
            data_array.append(sentence[:-2])

    return data_array

class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        sentences = self.nltk_splitter.tokenize(text)
        tokenized = [self.nltk_tokenizer.tokenize(sentence) for sentence in sentences]

        return tokenized

class POSTagger(object):

    def __init__(self):
        pass

    def pos_tag(self, sentences):
        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        # adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

if __name__ == "__main__":
    # Positives and negative sets
    pos_data = _get_sentences(True)
    neg_data = _get_sentences(False)

    # New Split and Tagger object
    splitter = Splitter()
    pos_tagger = POSTagger()

    # Go through the sentences and tag
    for sentence in pos_data:
        print pos_tagger.pos_tag(splitter.split(sentence))
