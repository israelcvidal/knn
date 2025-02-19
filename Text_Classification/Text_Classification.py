import nltk
import xml.etree.ElementTree as ET
import numpy as np
import nltk.classify.decisiontree as dt
import math
from sklearn.utils import shuffle

# In the first execution is necessary to download packets from nltk:
# nltk.download()

# reading the xml file with ElementTree and getting the root
tree = ET.parse('news_data.xml')
root = tree.getroot()
stemer = nltk.stem.RSLPStemmer()

# setting words to ignore in the classification
stopwords = nltk.corpus.stopwords.words("portuguese")
special_symbols = [',', '.', '(', ')', '!', '?', '@', '&', '*', ';', ':']


features = []
labels = []

# getting 'category' and 'text' from each item of the xml
for item in root.findall('item'):
    category = item.get('category')
    text = item.find("text").text
    title = item.find("title").text
    description = item.find("description").text

    #getting all words - except the ones in stopwords and special_symbols - from each text, title and description as a list and adding it do 'features'
    #in the same position as the respective label in the list 'labels'
    new_text = []
    if type(title) is unicode:
        words = nltk.word_tokenize(title)
        for w in words:
            if w not in stopwords and w not in special_symbols:
                new_text.append(stemer.stem(w.lower())) 

    if type(description) is unicode:
        words = nltk.word_tokenize(description)
        for w in words:
            if w not in stopwords and w not in special_symbols:
                new_text.append(stemer.stem(w.lower())) 

    if type(text) is unicode: 
    	words = nltk.word_tokenize(text)
        for w in words:
            if w not in stopwords and w not in special_symbols:
                new_text.append(stemer.stem(w.lower())) 

    features.append(new_text)
    labels.append(category)
  
#number of features we want to consider from the words selected from each text
numberOfFeatures = 10
top_features = []
data = []

#setting the new set of features 'top_features' as the numberOfFeatures most frequent words in each text
for line in features:
	top_features.append([x[0] for x in  nltk.FreqDist(line).most_common(numberOfFeatures)])

#making a dictionary for each text with the important words from that text as key and value 'True':
# {word='True'}
# after setting the dictionary of a text, we add the tuple (dictionary,label) to the new data set
for features, label in zip(top_features, labels):
	D = {}
	for feature in features:
		D[feature] = True
	data.append((D,label))

# now we have our data set as a list [(dict,label)] of each text, we can split the data set into tr and tt sets. 
ls = int(math.floor(len(data)*0.7))
# data = shuffle(data, random_state=0)
tr = data[:ls]
tt = data[ls:]

# we can now classify our data:
print 'Using the %d most frequent words to classify.' %numberOfFeatures
# classifier = nltk.NaiveBayesClassifier.train(tr)
# print 'NaiveBayes: ' + str(nltk.classify.accuracy(classifier,tt))

classifier = nltk.DecisionTreeClassifier.train(tr)
print 'DecisionTree: ' + str(nltk.classify.accuracy(classifier,tt))