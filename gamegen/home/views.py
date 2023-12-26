from django.views import generic
from django.urls import reverse_lazy
from modelclasses import models
from . import forms
from django.views.generic import TemplateView
from django.shortcuts import render
import requests
from xml.etree import ElementTree



class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        print("In Context Data")
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["games"] = models.game.objects.all()
        context["locations"] = models.location.objects.all()
        context["genres"] = models.genre.objects.all()
        context["teamings"] = models.teaming.objects.all()
        return context
    
class CreateGameView(TemplateView):
    template_name = "home/add_game.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["games"] = models.game.objects.all()
        context["locations"] = models.location.objects.all()
        context["genres"] = models.genre.objects.all()
        context["teamings"] = models.teaming.objects.all()
        return context
    
def gameTable(request):
    if(request.GET.get('location')and int(request.GET.get('location'))!=0):
        location = models.location.objects.get(id=request.GET.get('location'))
        games = location.game.all()
    else:
        games = models.game.objects.all()
    
    if(request.GET.get('genre')):
        # genre = models.genre.objects.get(id=request.GET.get('genre'))
        print("Genre")
        print(request.GET.getlist('genre'))
        games = games.filter(genre__in=request.GET.getlist('genre'))
    
    if(request.GET.get('player')and int(request.GET.get('player'))!=0):
        player = int(request.GET.get('player'))
        games = games.filter(min_player__lte=player, max_player__gte=player)
    
    if(request.GET.get('teaming')):
        games = games.filter(teaming__in=request.GET.getlist('teaming'))
    
    if(request.GET.get('duration') and int(request.GET.get('duration'))!=0):
        games = games.filter(duration__lte=int(request.GET.get('duration')))


    context = {'games': games}
    return render(request, 'home/game_table.html', context)

def addDislikes(request):
    disliker = []
    if(request.GET.get('location') and (request.GET.get('location')).isdigit() and int(request.GET.get('location'))!=0):
        location = models.location.objects.get(id=request.GET.get('location'))
        print("location")
        print(location)
        if location:
            print(location.disliker)
            disliker = location.disliker.split(",")
    context = {'dislikes': disliker}
    return render(request, 'home/add_dislike.html', context)


def loadFromBGG(request):
    dataDict = {}
    gameID = request.GET.get('id')
    url = "https://boardgamegeek.com/xmlapi2/thing/?id="+gameID
    data = requests.get(url)
    tree = ElementTree.fromstring(data.content)
    print("Data")
    print(tree[0].__dir__())
    print(tree[0])
    print(tree[0].items())
    print(tree[0].find("playingtime"))
    print(tree[0].find("playingtime").attrib["value"])
    dataDict["name"]=tree[0].find("name").attrib["value"]
    dataDict["duration"]=tree[0].find("playingtime").attrib["value"]
    dataDict["minPlayer"]=tree[0].find("minplayers").attrib["value"]
    dataDict["maxPlayer"]=tree[0].find("maxplayers").attrib["value"]
    context = {"data": dataDict}
    return render(request, 'home/game_data_htmx.html', context) # Check if can be used for expansion too 