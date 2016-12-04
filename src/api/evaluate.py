import re, math, collections, itertools
import nltk
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet as swn
import yaml

def _get_sentences(is_positive):
    if is_positive:
        data = open('dataset/positives.txt', 'r')
        pos_or_neg = '1'
    else:
        data = open('dataset/negatives.txt', 'r')
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

class DictionaryTagger(object):

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        tag_sentence = []

        for (word, lemma, postag) in sentence:
            tag = self.wordnet_pos_code(postag[0])
            senti_word = swn.senti_synsets(word)
            pos_score = 0.0
            neg_score = 0.0
            for sw in senti_word:
                pos_score += sw.pos_score()
                neg_score += sw.neg_score()
            s = (word, lemma, postag, pos_score, neg_score)
            tag_sentence.append(s)
        return tag_sentence

    # Translation from nltk to Wordnet
    def wordnet_pos_code(self, tag):
        if tag.startswith('NN'):
            return wordnet.NOUN
        elif tag.startswith('VB'):
            return wordnet.VERB
        elif tag.startswith('JJ'):
            return wordnet.ADJ
        elif tag.startswith('RB'):
            return wordnet.ADV
        else:
            return ''

def sentiment_score(sentence):    
    sentence = sentence[0]
    score = 0
    for (word, lemma, postag, pos_score, neg_score) in sentence:
        score += pos_score
        score -= neg_score

    return score

if __name__ == "__main__":
    # Positives and negative sets
    pos_data = _get_sentences(True)
    neg_data = _get_sentences(False)

    # New Split and Tagger object
    splitter = Splitter()
    pos_tagger = POSTagger()
    dicttagger = DictionaryTagger()

    # pos_tagged_sentences = [[('Every', 'Every', ['DT']), ('time', 'time', ['NN']), ('I', 'I', ['PRP']), ('eat', 'eat', ['VBP']), ('here', 'here', ['RB']), (',', ',', [',']), ('I', 'I', ['PRP']), ('see', 'see', ['VBP']), ('caring', 'caring', ['VBG']), ('teamwork', 'teamwork', ['NN']), ('to', 'to', ['TO']), ('a', 'a', ['DT']), ('professional', 'professional', ['JJ']), ('degree', 'degree', ['NN']), ('.', '.', ['.'])]]
    # print dicttagger.tag(pos_tagged_sentences)

    # Go through the sentences and tag
    for sentence in pos_data:
        tagged_sentence = dicttagger.tag(pos_tagger.pos_tag(splitter.split(sentence)))
        print sentence, sentiment_score(tagged_sentence)
