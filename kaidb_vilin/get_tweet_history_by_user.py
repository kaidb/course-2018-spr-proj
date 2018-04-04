"""
Tweepy python script used to retrieve all tweets from a particular user
@Author: Kai Bernardini

Tweepy -- https://github.com/tweepy/tweepy
adapted from. -- (TODO: link to github)
"""
import tweepy 
# I/O read/writes
import pandas as pd

#Twitter API credentials
# Do not leave values hardcoded 
consumer_key = "fm6ta9Ixfhzn7FdkmIL2VRowh"
consumer_secret = "3I3m6BWs380cN5aRN3Sz5vAZNqAddv5GUBoSu14mjb1FL1Eve5"
access_key = "967989243674062848-5LuNrFlSZxopGdleeW3iszkNigUeuI0"
access_secret = "HYc0kOOhclP0FWZ5xhr3bOx0SsatVVcBQrzADBTN9dG60"

def get_all_tweets(screen_name, use_pandas = False):
	"""Retrieve all tweets froma. particular users by their username
	- Notes: Twitter will on ly store the last 3,240 tweets from a particular 
	user using standard Dev creds. """
    
    # Authorization and initialization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a  dumb-list to hold scraped tweets
    alltweets = []  
    # Get first 200 tweets 
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    # This tells us where to begin our search 
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print( "getting tweets before %s" % (oldest))
        
        #all subsiquent requests use the max_id param to prevent duplicates
        # We can only get at most 200 tweets per querry
        # BONUS: twitter doesn't appear to limit this. 
        # Make sure caching is enabled as to not prevent duplicate querries 
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print( "...{} tweets downloaded so far".format(len(alltweets)))
    if use_pandas:
    	AT = [alltweets[i]._json for i in range(len(alltweets))]
    	data = pd.DataFrame(AT)
    	return data 

    return alltweets
