import tweepy

from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
        if request.method == 'POST':
            content = request.POST.get('content', '')

            if content:
                print('Content', content)

                auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
                auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
                api = tweepy.API(auth)
                api.update_status(content)

                return redirect('index')

        return render(request,'post.html')