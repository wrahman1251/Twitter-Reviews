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

user = "suaixuan"

statuses = api.GetUserTimeline(screen_name=user)

for s in statuses:
	print extract_words(s.text)