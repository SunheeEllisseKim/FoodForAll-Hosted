import tweepy

from django.conf import settings
from django.shortcuts import render, redirect
from home.forms import DonorForm
from django.http import HttpResponseRedirect
# Create your views here.

def tweet(request):
    form = ''
    submitted = False
    
    if request.method =='POST':
        if 'tweet' in request.POST:
            print("hello")
            content = request.POST.get('content', '')

            if content:
                print('Content', content)

                auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
                auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
                api = tweepy.API(auth)
                api.update_status(content)
                return redirect('post') 

            return render(request,'post.html')
        elif 'contact' in request.POST:

            form = DonorForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/post.html?submitted=True')
    else:
        form = DonorForm
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request,'post.html',{'form' : form, 'submitted' : submitted})
    
    
    
    '''
    if request.method == 'POST':
            content = request.POST.get('content', '')

            if content:
                print('Content', content)

                auth = tweepy.OAuthHandler(settings.API_KEY, settings.API_KEY_SECRET)
                auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
                api = tweepy.API(auth)
                api.update_status(content)

                return redirect('tweet')

        return render(request,'post.html')
    '''
        
'''
def contact(request):
    submitted = False
    if request.method =='POST':
        form = DonorForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/post.html?submitted=True')
        else:
            form = DonorForm
            if 'submitted' in request.GET:
                submitted = True
    
    return render(request,'post.html',{'form' : form, 'submitted' : submitted})
'''        
