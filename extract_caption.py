import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text 
import json

# collect all captions from result.json
with open('result.json') as data_file:
    caption = []
    data = json.load(data_file)
    for i in range(0,85):
        for j in data[str(i)]["posts"]:
            caption.append(data[str(i)]["posts"][str(j)]["caption"])
    #print '\n'.join(c for c in caption)

# process caption as a bag of words
count_vector = CountVectorizer(analyzer="word",stop_words="english")
train_data_features = count_vector.fit_transform(caption)
train_data_features = train_data_features.toarray()

# look at the words in the vocabulary
vocab = count_vector.get_feature_names()

# sum up the counts of each vocabulary word
dist = np.sum(train_data_features, axis=0)

# count the number of times each vocabulary word appears in the training set
final_dict = {}
for word, count in zip(vocab, dist):
	final_dict[word] = count
final_dict = sorted(final_dict.items(), key=lambda x: x[1])

# save data in vocab.json
with open('vocab.json', 'w') as file:
	json.dump(final_dict, file)

# testing sorting
for word, count in final_dict:
	print count, word