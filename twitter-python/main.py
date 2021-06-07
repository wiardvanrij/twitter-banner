import tweepy
import os
import requests


consumer_key =os.environ['consumer_key']
consumer_secret =os.environ['consumer_secret']
access_token =os.environ['access_token']
access_token_secret =os.environ['access_token_secret']
image_url =os.environ['image_url']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

request = requests.get(image_url)

if not request.ok:
    print("failed to fetch image")
    print(request.text)
    exit()

img_data = request.content

with open('twitter_banner.png', 'wb') as handler:
    handler.write(img_data)

api = tweepy.API(auth)
api.update_profile_banner('twitter_banner.png')
