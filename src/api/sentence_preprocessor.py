import re
import nltk

class Preprocessor:

    def __init__(self):
        print "Preprocessor initialized"
        self.HAPPY = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'
            ])

        self.SAD = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
            ])
        self.negtn_regex = re.compile( r"""(?:
                ^(?:never|no|nothing|nowhere|noone|none|not|
                    havent|hasnt|hadnt|cant|couldnt|shouldnt|
                    wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
                )$
            )
            |
            n't
            """, re.X)

    def preprocess_tuple(self, tweet):
        sentence = tweet[0]
        sentence = self.preprocess(sentence)
        return (sentence, tweet[1])

    def preprocess(self, sentence):
        sentence = sentence.lower()
        sentence = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',sentence) # convert url
        sentence = re.sub('@[^\s]+','AT_USER',sentence) # convert @
        sentence = re.sub('[\s]+', ' ', sentence) # remove white spaces
        sentence = re.sub(r'#([^\s]+)', r'\1', sentence) # replace hashtags
        sentence = sentence.replace('.', '').replace(',', '').replace('!', '').replace('?', '')
        sentence = sentence.rstrip('\'"') # removed quotes
        sentence = sentence.lstrip('\'"')
        return sentence

    def mark_negation(self, sentence):
        negated_sentence = []
        # print sentence
        sentence = [ word for word in sentence if not type(word) == tuple]
        for word in sentence:
          if self.negtn_regex.search(word):
            negated_sentence.append(word + '_NEG')
        return negated_sentence

    def mark_emoticons(self, sentence):
        emotion_sentence = []
        sentence = [ word for word in sentence if not type(word) == tuple]
        for word in sentence:
          if word in self.HAPPY:
            emotion_sentence.append('happy')
          if word in self.SAD:
            emotion_sentence.append('sad')
        return emotion_sentence

    def mark_pos_tag(self, sentence):
        pos_tagged_sentence = []
        sentence = [ word for word in sentence if not type(word) == tuple]
        return [ word[1] for word in nltk.pos_tag(sentence)]

