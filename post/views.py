import tweepy
from home.forms import DonorForm
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

# Create your views here.

def CreateTweet(request):
        donation = ''
        submitted = False

        if request.method == 'POST':
            donation = DonorForm(request.POST)
            if donation.is_valid():
                donation.save()
                
                content = donation.cleaned_data.get('DonorTwitter')
            

            #if content:
                print('Content', content)

                # auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
                # auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
                # api = tweepy.API(auth)
                # api.update_status(content)
                client = tweepy.Client(consumer_key=settings.API_KEY, consumer_secret=settings.API_KEY_SECRET, access_token=settings.ACCESS_TOKEN, access_token_secret=settings.ACCESS_TOKEN_SECRET)
                response = client.create_tweet(text=content)
                return HttpResponseRedirect('/post?submitted=True')
                # return redirect('index')
        else:
            donation = DonorForm
            if 'submitted' in request.GET:
                submitted = True
        # return
        return render(request,'post.html',{'donation' : donation, 'submitted' : submitted})
