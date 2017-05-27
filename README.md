# TweetAlert

Two components in one simple python file:
+ /listen - the _Listener_ - Filters Twitter firehose for Tweets of interest, Tweets within areas of interest. 
  + Real-time PowerTrack stream consumer - Receives Tweets within a few seconds of being posted.  
+ /notify - sends notification Direct Messages with Twitter DM API.

The TweetAlert, along with Enroller below, make up an example Twitter-based, geo-ware notification system.
+ /enroll - the _Enroller_ - Twitter Account Activity Webhook consumer, subscribers share location privately.
  + PowerTrack Rules Manager - Creates and manages subscriber-specific PowerTrack filters. 
