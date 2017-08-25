#!/usr/bin/env python
from gnippy import PowerTrackClient #HTTP stream managed by Gnippy, a fine manager for low-volume streams.
import time
import datetime
import os
import json
from twitter import Twitter, OAuth

# Define a callback
def callback(activity):

    print('Received Tweet, preparing Direct Message...') #to standard out.
    print(activity)

    #Parse the things we need: who posted it, when it was posted, what rules/subscribers matched it?  And a link to the Tweet. 
    tweet_hash = json.loads(activity)
    created_time_str = tweet_hash['created_at']

    author = tweet_hash['user']['screen_name']
    #user_id = tweet_hash['user']['id_str']
    
    #https://twitter.com/FloodSocial/status/868250610742722561
    tweet_link = "https://twitter.com/" + author + "/status/" + tweet_hash['id_str']

    #Let's do some tweet-posted to response-tweet latency.
    time_created = datetime.datetime.strptime(created_time_str,'%a %b %d %H:%M:%S +0000 %Y')
    time_now = datetime.datetime.utcnow()
    seconds = (time_now - time_created).total_seconds()
    
    #Construct Direct Message Notification.
    message = "@" + author + " posted a Tweet within an area of your interest! \nTweet contents: " + tweet_hash['text'] + " |\nTweet link: " + tweet_link + " |\nNotification sent in " + str(seconds) + " seconds."

    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['ACCESS_SECRET']

    t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

    recipients = tweet_hash['matching_rules']
    print(recipients)
    
    for recipient in recipients:
        user_tag = recipient['tag']
        recipient_id = user_tag.split('|')[0]

        # Send a direct message
        t.direct_messages.new(user=recipient_id, text=message)
    
        print('Sent Direct Message to ' + str(recipient_id) + ': ' + message)
 
#------------------------------------------------   
# Create the client

print("Starting up")

#Load config.
#If local config file, use that. If no file (e.g. on Heroku), load from environmental variables.

user_name = os.environ['GNIP_USER_NAME']
password = os.environ['GNIP_PASSWORD']
account_name = os.environ['GNIP_ACCOUNT_NAME']
label = os.environ['GNIP_LABEL']

my_url = 'https://gnip-stream.twitter.com/stream/powertrack/accounts/' + account_name + '/publishers/twitter/' + label + '.json'
print(my_url)

client = PowerTrackClient(callback, url=my_url, auth=(user_name, password))
client.connect()

print("Starting to stream...")

while True:
  x = 1  
  
  
