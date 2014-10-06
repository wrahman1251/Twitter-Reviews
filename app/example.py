#import numpy as np
from math import pow, exp
import twitter
from string import ascii_letters

api = twitter.Api(consumer_key='anQXwx7bfYW82vdSUnWD1Sqtx', consumer_secret='MktlZBECkhFTZKd8Pr2XAVhy4zcHA3LDftHLJlKAsbd3sMYGKD', access_token_key='359708424-GwkMKGJxPmNMi1ucW6QA5ZlclJPb7SGxT3rGJg7h', access_token_secret='NDLFEAipd7VgpJbVN4JVlaDM7xx7hYhHSAsWszoORZzU2')

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    "*** YOUR CODE HERE ***"
    for i in range(len(text)):
        if text[i] not in ascii_letters:
            text = unicode.replace(text, text[i], ' ')
    return text.encode("ascii").split()

#user = "negative_nedder"

#statuses = api.GetUserTimeline(screen_name=user, count=100, exclude_replies=False)



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

def main():
    # We load in the list of words and their log probabilities
    happy_log_probs, sad_log_probs = readSentimentList('twitter_sentiment_list.csv')

    # Here we have tweets which we have already tokenized (turned into an array of words)
    tweet1 = ['I', 'love', 'holidays']
    tweet2 = ['very', 'sad']

    # Calculate the probabilities that the tweets are happy or sad
    #tweet1_happy_prob, tweet1_sad_prob = classifySentiment(tweet1, happy_log_probs, sad_log_probs)
    #tweet2_happy_prob, tweet2_sad_prob = classifySentiment(tweet2, happy_log_probs, sad_log_probs)
    
    #print "The probability that tweet1 (", tweet1, ") is happy is ", tweet1_happy_prob, "and the probability that it is sad is ", tweet1_sad_prob
    #print "The probability that tweet2 (", tweet2, ") is sad is ", tweet2_happy_prob, "and the probability that it is sad is ", tweet2_sad_prob

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
        return decision + advice

    else:
        decision = '-'
        advice = 'Stay the f*** away from this person. DANGER DANGER!'
        return decision + advice

if __name__ == '__main__':
    main()
