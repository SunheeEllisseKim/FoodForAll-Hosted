from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.

def get_food(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')

        if content:
            print('Content', content)

            return redirect('index')

    return render(request,'')