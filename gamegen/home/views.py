from django.views import generic
from django.urls import reverse_lazy
from modelclasses import models
from . import forms
from django.views.generic import TemplateView
from django.shortcuts import render
import requests
from xml.etree import ElementTree
from django.http import HttpResponse



class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        user =self.request.user
        games = editableGames(user)
        userLocations = list(user.viewer.all())
        for location in userLocations:
            games = list(set(games) | set(location.game.all()))
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["games"] = games
        context["locations"] = list(user.creater.all()) + list(user.editer.all()) + list(user.viewer.all())
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
        context["locations"] = list(self.request.user.creater.all()) + list(self.request.user.editer.all())
        context["genres"] = models.genre.objects.all()
        context["teamings"] = models.teaming.objects.all()
        return context
    
class CreateExpansionView(TemplateView):
    template_name = "home/add_game.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["games"] = models.expansion.objects.all()
        context["locations"] = list(self.request.user.creater.all()) + list(self.request.user.editer.all())
        context["genres"] = models.genre.objects.all()
        context["teamings"] = models.teaming.objects.all()
        context["type"] = "expansion"
        context["allGames"] = models.game.objects.all()
        return context


def gameTable(request):
    user =request.user
    games = editableGames(user)
    userLocations = list(user.viewer.all())
    if(request.GET.get('location')and int(request.GET.get('location'))!=0):
        location = models.location.objects.get(id=request.GET.get('location'))
        games = location.game.all()
    else:
        for location in userLocations:
            games = list(set(games) | set(location.game.all()))
    
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
        if location:
            disliker = location.disliker.split(",")
    context = {'dislikes': disliker}
    return render(request, 'home/add_dislike.html', context)


def loadFromBGG(request):
    dataDict = {}
    gameID = request.GET.get('id')
    url = "https://boardgamegeek.com/xmlapi2/thing/?id="+gameID
    data = requests.get(url)
    tree = ElementTree.fromstring(data.content)
    dataDict["name"]=tree[0].find("name").attrib["value"]
    dataDict["duration"]=tree[0].find("playingtime").attrib["value"]
    dataDict["minPlayer"]=tree[0].find("minplayers").attrib["value"]
    dataDict["maxPlayer"]=tree[0].find("maxplayers").attrib["value"]
    context = {"data": dataDict}
    context["locations"] = models.location.objects.all()
    context["genres"] = models.genre.objects.all()
    context["teamings"] = models.teaming.objects.all()
    context["type"] = request.GET.get('type')
    if context["type"]=="expansion":
        context["allGames"] = models.game.objects.all()
    return render(request, 'home/game_data_htmx.html', context) # Check if can be used for expansion too 

def saveNewGame(request):
    type = request.POST.get('type')
    name = request.POST.get('name')
    duration = request.POST.get('duration')
    minPlayer = request.POST.get('minPlayer')
    maxPlayer = request.POST.get('maxPlayer')
    releaseDate = request.POST.get('releaseDate')
    ruleLink = request.POST.get('ruleLink')
    # ruleFile = request.FILES["ruleFile"]
    genres = request.POST.getlist('genre')
    teamings = request.POST.getlist('teaming')


    if type=="expansion":
        baseGame = models.game.objects.get(id=request.POST.get('baseGame'))
        number = request.POST.get("number")
        game = models.expansion(name=name, base_game=baseGame, number=number, duration=duration, min_player=minPlayer, max_player=maxPlayer, rule_link=ruleLink)
        game.save()
    else:
        game = models.game(name=name, duration=duration, min_player=minPlayer, max_player=maxPlayer, rule_link=ruleLink)
        game.save()
    game.genre.set(genres)
    game.teaming.set(teamings)

    if releaseDate:
        game.release_date=releaseDate
    if "ruleFile" in request.FILES:
        game.file = request.FILES["ruleFile"]

    game.save()
    return HttpResponse(status=200)

def addGame(request):
    locationID = request.GET.get('location')
    if isinstance(locationID, int):
        location = models.location.objects.get(id=locationID)
    else:
        location = models.location(creater = request.user, name=locationID)
        location.save()

    # check if location int, if not, create location with user as creater


    if request.GET.get('type')=="expansion":
        expansion = models.expansion.objects.get(id=request.GET.get('game'))
        location.expansions.add(expansion)
        location.save()
        pass
    else:
        game = models.game.objects.get(id=request.GET.get('game'))
        dislikes = request.GET.getlist('dislike')
        dislikeString = ','.join(dislikes)
        existingDislike = models.dislikes.objects.filter(location=location, game=game)
        if existingDislike:
            return HttpResponse(status=200)
        dislike = models.dislikes(game=game, location=location, disliker=dislikeString)
        dislike.save()
        locationDislikes = str(location.disliker)
        ### Check if every disliker in location.dislikes
        for dislikeObject in dislikes:
            if dislikeObject not in locationDislikes:
                locationDislikes = locationDislikes + ", "+dislikeObject

        location.disliker = locationDislikes
        location.save()
    return HttpResponse(status=200)

def editableGames(user):
    games = []
    locations = list(user.creater.all()) + list(user.editer.all())
    for location in locations:
        games = list(set(games) | set(location.game.all()))
    return games