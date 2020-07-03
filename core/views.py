from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DictionaryForm
from django.http import HttpResponse
from django.conf import settings
import requests
from json import dumps
from .models import Dictionary
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

'''
def web(request):
    try:
        if request.user.is_authenticated:
            return redirect("core:home")
        else:
            return redirect("core:oxford")
    except:
        return render(request, 'core/web.html')
'''

def searchLogic(request):
    search_result = {}
    if 'word' in request.GET:
        form = DictionaryForm(request.GET)
        if form.is_valid():
            search_result = form.search()
            if request.user.is_authenticated and search_result['success'] and not Dictionary.objects.filter(user = request.user, word=request.GET['word'].lower()).first():
                Dictionary.objects.create(user=request.user, word = request.GET['word'].lower(),
                 defination=search_result['results'][0]['definition'])
    else:
        form = DictionaryForm()

    return (search_result, form)

@login_required()
def home(request):
    search_result, form = searchLogic(request)
    history = Dictionary.objects.filter(user = request.user)
    return render(request, 'core/home.html', {'form': form, 'search_result': search_result,'history':history})


def web(request):
        if request.user.is_authenticated:
            return redirect("core:home")
        else:
            search_result, form = searchLogic(request)
            return render(request, 'core/web.html', {'form': form, 'search_result': search_result})


@csrf_exempt
def search(request):
    if request.method == "POST":
        letter = request.POST.get('letter')
        url = "https://wordsapiv1.p.rapidapi.com/words/"
        pattern = "^{}".format(letter)
        query = {"letterPattern": pattern, "limit":"10"}
        headers = {
            'x-rapidapi-host': settings.API_HOST,
            'x-rapidapi-key': settings.API_KEY
        }
        response = requests.request(
            "GET", url, headers=headers, params=query)
        res = response.json()['results']
        if response.status_code == 200:  # SUCCESS
            result = response.json()['results']

        else:
            result= None
    return HttpResponse(dumps(result))
