# twitter-sentiment-analysis
Twitter Sentiment Analysis - This simple algorithm to calculate sentiment was written during Artificial Intelligence course CS4100.
pip install nltk

##Approach
Our approach to building this tool began with finding an existing dataset of tagged “positive” and “negative” sentences that could be utilized for training and testing purposes. We found our dataset on the UCI Machine Learning Repository. The next step was to write functions that would preprocess these sentences, and eventually tweets. In preprocessing, we first got rid of the ‘@user’, ‘#’, and ‘RT’ features in any tweet. We also disregarded any other URLs that were part of the tweet, since we didn’t feel that those URLs would play a role in finding the sentiment of a sentence. After removing those items, we removed any extra white spaces in the the sentence, along with any punctuation. For words that contained three or more repeated letters, we removed extra letters so that the word would only have a maximum of two repeated letters. For example, if we saw the word “haaaaaate”, we would change that to “haate”. One reason for this is that there are never more than two of the same letter repeated twice in English. In addition, the repetition of some letters are used as a way to show emotion by putting a linguistic stress on the syllable in which the repeated letters are in. After this, we did some tokenization of the sentences as well as removed stop words. We used NLTK python library to do this for each sentence. Next, we used a variety of features to capture more information for classification purposes. The features we included were positive/negative words, bigrams, emoticon translation, and negations. We had some pre-defined emoticons for both positive and negative sentiments that we kept track of. We would keep checking if these emoticones occurred anywhere in the tweet. If so, we would add happy or sad feature if one of emoticons from positive or negative emoticons lists was in a sentence. 

We also checked for negation. Any words ending with “n't", and ‘not’, ‘cannot’ and ‘no’ were all replaced with ‘_NEG’ to mark that its negation. Another feature we used, as mentioned before, was bigrams. We paired every two words together to further catch the text classification. We then used the Naive Bayes Classifier in order to do training and classification on our dataset. Naive Bayes Classifier uses vectors of features to assign class labels to problems. We would then use trained classifier to predict sentiment for unknown dataset. Lastly, we classified tweets using the Twitter API by geolocation. We used the Twitter API for searching by geolocation so we could compare and contrast general sentiments in different cities in the USA. We focused in on tweets from 6 different cities, 3 from each coast (east and west). A further extension of our project could be to make some kind of visual representation or infographic that would show the differences in sentiment across a map of the USA or the world. 
