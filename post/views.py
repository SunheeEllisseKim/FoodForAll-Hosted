import tweepy

from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.

def CreateTweet(request):
        if request.method == 'POST':
            content = request.POST.get('content', '')

            if content:
                print('Content', content)

                # auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
                # auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
                # api = tweepy.API(auth)
                # api.update_status(content)
                client = tweepy.Client(consumer_key=settings.API_KEY, consumer_secret=settings.API_KEY_SECRET, access_token=settings.ACCESS_TOKEN, access_token_secret=settings.ACCESS_TOKEN_SECRET)
                response = client.create_tweet(text=content)

                # return redirect('index')

        # return
        return render(request,'post.html')