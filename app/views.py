from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g
from app import app
from example import extract_words
import twitter
from math import pow, exp

api = twitter.Api(consumer_key='anQXwx7bfYW82vdSUnWD1Sqtx', consumer_secret='MktlZBECkhFTZKd8Pr2XAVhy4zcHA3LDftHLJlKAsbd3sMYGKD', access_token_key='359708424-GwkMKGJxPmNMi1ucW6QA5ZlclJPb7SGxT3rGJg7h', access_token_secret='NDLFEAipd7VgpJbVN4JVlaDM7xx7hYhHSAsWszoORZzU2')


@app.route('/')
@app.route('/index')
def my_form():
	return render_template("my-form.html", name='Home')
def classifySentiment(words, happy_log_probs, sad_log_probs):
		# Get the log-probability of each word under each sentiment
		happy_probs = [happy_log_probs[word] for word in words if word in happy_log_probs]
		sad_probs = [sad_log_probs[word] for word in words if word in sad_log_probs]

		# Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
		tweet_happy_log_prob = sum(happy_probs)
		tweet_sad_log_prob = sum(sad_probs)

		# Calculate the probability of the tweet belonging to each sentiment
		prob_happy = 1/(exp(tweet_sad_log_prob - tweet_happy_log_prob) + 1)
		prob_sad = 1 - prob_happy

		return prob_happy, prob_sad
def readSentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() #Ignore title row
    
    for line in ifile:
        tokens = line[:-1].split(',')
        happy_log_probs[tokens[0]] = float(tokens[1])
        sad_log_probs[tokens[0]] = float(tokens[2])

    return happy_log_probs, sad_log_probs


@app.route('/', methods=['POST'])

def my_form_post():
	user = request.form['text']
	statuses = api.GetUserTimeline(screen_name=user, count=100, exclude_replies=False)

	# We load in the list of words and their log probabilities
	happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')
	pos_lst = []
	neg_lst = []
	for s in statuses:
		tweet_happy_prob, tweet_sad_prob = classifySentiment(extract_words(s.text), happy_log_probs, sad_log_probs)
		pos_lst.append(tweet_happy_prob)
		neg_lst.append(tweet_sad_prob)

   	pos_avg = sum(pos_lst)/len(pos_lst)
   	neg_avg = sum(neg_lst)/len(neg_lst)

   	if pos_avg > neg_avg:
   		decision = '+'
   		if pos_avg > (neg_avg + 0.2):
   			advice = 'This person is REALLY positive. Become frnd nao!'
   		else:
   			advice = 'This person is not full of sunshine but I guess they are aite'
   		return decision, advice
   	else:
   		decision = '-'
   		advice = 'Stay the f*** away from this person. DANGER DANGER!'
   		return decision, advice

	if __name__ == '__main__':
		form_post()



if __name__=='__main__':
	app.run()

