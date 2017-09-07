# instagram-predictor
The goal of Instagram Predictor is to use user profile data with basic post data to help the average social media user make informed decisions about their Instagram posts.

## What does Instagram Predictor do?
* Predicts popularity of instagram posts by scraping posts and analyzing 12 features of each post
* Trains dataset in 5 different machine learners with 10-fold cross validation 
* Uses Python, Scikit-learn, Weka and Instgram API
* More detailed report can be found [here](https://spark.adobe.com/page/eDAdXRsCYlteX/)
* This project was done with my project partner [Jessica Li](jessicali1.2018@u.northwestern.edu) and mentor [Professor Downey](https://www.cs.northwestern.edu/~ddowney/) in EECS 349: Machine Learning at Northwestern University

## What are features? 
For this project, we include user profile data along with data of each post to customize prediction for each user. Here is a list of features we used.

1. num_posts
2. total_comments
3. num_insta_tags
4. num_followers
5. num_followings
6. comments
7. num_emoji
8. num_tags
9. caption_length
10. total_likes
11. location
12. date

## What else should we know about Instagram Predictor?
We used Scrapy, a web crawling framework for Python, to crawl a total of 1770 Instagram posts from 103 college age Instagram users. Because most of users we gathered data from are our friends, we did not include few files to protect their privacy. These files are 'result.csv', 'result.json' and 'vocab.json'. 'result.csv' is a final dataset in CSV format where each row lists 12 features of a post. 'result.json' is a dataset in JSON format which is converted from 'result.csv' file. 'vocab.json' is a dataset of all words in "caption" of posts in JSON format. Specifically, we processed caption as a bag of words(vector array) and counted the number of times each vocabulary word appears in the training set. 
