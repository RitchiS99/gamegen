from django.views import generic
from django.urls import reverse_lazy
from modelclasses import models
from . import forms
from django.views.generic import TemplateView
from django.shortcuts import render
import requests
from xml.etree import ElementTree
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
# from django.template import loader


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user =self.request.user
        if user.is_authenticated:
            locations = (user.creater.all() | user.editer.all() | user.viewer.all()).distinct()
            location = locations.first()
            games = location.game.all()
            userLocations = list(user.viewer.all())
            for location in userLocations:
                games = list(set(games) | set(location.game.all()))
            dislikes = models.dislikes.objects.filter(game__in=games, location=location)
            context["games"] = dislikes
            context["locations"] = locations
            context["selectedLocation"] = location
            context["location"] = location
            context["type"]="collection"
        else:
            context["games"] = []
            context["locations"] = []
        # Call the base implementation first to get a context

        # Add in a QuerySet of all the books

        context["genres"] = models.genre.objects.all()
        context["teamings"] = models.teaming.objects.all()
        return context
    
    
class CreateGameView(LoginRequiredMixin,TemplateView):
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
    
class CreateExpansionView(LoginRequiredMixin, TemplateView):
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
    typeValue = request.GET.get('type')
    user =request.user
    games = editableGames(user)
    locations = (user.creater.all() | user.editer.all() | user.viewer.all()).distinct()
    location = None
    if(request.GET.get('location')and int(request.GET.get('location'))!=0): # check if location in user.locations
        location = models.location.objects.get(id=request.GET.get('location'))
    else:
        location = locations.first()
    

    


    gameData = filterGames(request)
    print("Expansions")
    print(games)
    print(gameData["games"])
    

    context = {'games': gameData["games"], 'location': location, 'notGames': gameData["notGames"], 'expansions': gameData["expansions"], 'type':typeValue}
    return render(request, 'home/game_table.html', context)

def addDislikes(request):
    disliker = []
    if(request.GET.get('location') and (request.GET.get('location')).isdigit() and int(request.GET.get('location'))!=0):
        location = models.location.objects.get(id=request.GET.get('location'))
        if location and location.disliker:
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
    if locationID.isnumeric():
        location = models.location.objects.get(id=locationID)
    else:
        location = models.location(creater = request.user, name=locationID)
        location.save()

    # check if location int, if not, create location with user as creater


    if request.GET.get('type')=="expansion":
        id_list = request.GET.getlist('game')
        for id in id_list:
            expansion = models.expansion.objects.get(id=id)
            location.expansions.add(expansion)
            location.save()
        pass
    else:
        id_list = request.GET.getlist('game')
        for id in id_list:
            game = models.game.objects.get(id=id)
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
                    locationDislikes = locationDislikes + ","+dislikeObject

            location.disliker = locationDislikes
            location.save()
    return HttpResponse(status=200)

def editableGames(user):
    games = models.game.objects.none()
    locations = list(user.creater.all()) + list(user.editer.all())
    for location in locations:
        games = games | location.game.all()
    return games


def login(request, context={}):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('login.html')
    if request.method == 'GET':
        next = request.GET.get('next')
        context["next"] = next
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            next = request.POST.get('next')
            if next!="None":
                print("Next is next")
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/')
        else:
            # messages.error(request, 'Error wrong username/password')
            messages.error(request, 'Error wrong username/password')
    context[messages] = {
        'messages'
    }
    return render(request,'login.html', context=context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def addWishlist(request):
    locationID = request.GET.get('location')
    id_list = request.GET.getlist('game')
    if locationID.isnumeric():
        location = models.location.objects.get(id=locationID)
    else:
        location = models.location(creater = request.user, name=locationID)
        location.save()
    if request.GET.get('type')=="expansion":
        for id in id_list:
            expansion = models.expansion.objects.get(id=id)
            location.wishlist_expansions.add(expansion)
    else:
        for id in id_list:
            game = models.game.objects.get(id=id)
            location.wishlist_games.add(game)
    location.save()
    return HttpResponse(status=200)


def changeDislikes(request):
    game = models.game.objects.get(id=request.GET.get('game'))
    location = models.location.objects.get(id=request.GET.get('location'))
    dislikeList = list(models.dislikes.objects.get(game=game,location=location).disliker.split(","))
    dislikes = list(location.disliker.split(","))
    context = {'game': game, 'dislikeList': dislikeList, "dislikes":dislikes, "location":location}
    return render(request, 'home/change_dislike.html', context=context)

def changeDislikesSave(request):
    game = models.game.objects.get(id=int(request.GET.get('game')))
    location = models.location.objects.get(id=int(request.GET.get('location')))
    dislikes = request.GET.getlist('dislike')
    gameDislike = models.dislikes.objects.get(game=game, location=location)
    gameDislike.disliker = ','.join(dislikes)
    gameDislike.save()
    locationDislikes = str(location.disliker)
    ### Check if every disliker in location.dislikes
    for dislikeObject in dislikes:
        if dislikeObject not in locationDislikes:
            locationDislikes = locationDislikes + ","+dislikeObject
    location.disliker = locationDislikes
    location.save()
    return gameTable(request)

def addToStorage(request):
    typeValue = request.GET.get('elementType')
    location = models.location.objects.get(id=int(request.GET.get('location')))
    if typeValue=="game":
        game = models.game.objects.get(id=int(request.GET.get('game')))
        if not models.dislikes.objects.filter(game=game, location=location).exists():
            dislike = models.dislikes(game=game, location=location, disliker="")
            dislike.save()
        location.wishlist_games.remove(game)
        location.save()
    elif typeValue=="expansion":
        expansion = models.expansion.objects.get(id=int(request.GET.get('game')))
        location.expansions.add(expansion)
        location.wishlist_expansions.remove(expansion)
        location.save()
    return gameTable(request)



def deleteItem(request):
    typeFrom = request.GET.get('type')
    elementType = request.GET.get('elementType')
    location = models.location.objects.get(id=int(request.GET.get('location')))
    if typeFrom == "wishlist":
        if elementType=="game":
            game = models.game.objects.get(id=int(request.GET.get('game')))
            location.wishlist_games.remove(game)
        elif elementType=="expansion":
            expansion = models.expansion.objects.get(id=int(request.GET.get('game')))
            location.wishlist_expansion.remove(expansion)
    elif typeFrom == "collection":
        if elementType=="game":
            game = models.game.objects.get(id=int(request.GET.get('game')))
            dislike = models.dislikes.objects.get(location=location, game=game)
            dislike.delete()
        elif elementType=="expansion":
            expansion = models.expansion.objects.get(id=int(request.GET.get('game')))
            location.expansions.remove(expansion)
    location.save()
    return gameTable(request)


def filterGames(request):
    typeValue = request.GET.get('type') or 'collection'
    user =request.user
    games = editableGames(user)
    locations = (user.creater.all() | user.editer.all() | user.viewer.all()).distinct()
    expansions = None
    expansionGames = None
    location = None
    notGames = None
    if(request.GET.get('location')and int(request.GET.get('location'))!=0): # check if location in user.locations
        location = models.location.objects.get(id=request.GET.get('location'))
        if typeValue=="wishlist":
            games = location.wishlist_games.all()
            expansions = location.wishlist_expansions.all()
        else:
            games = location.game.all()
            expansions = location.expansions.all()
    else:
        location = locations.first()
        if typeValue=="wishlist":
            games = location.wishlist_games.all()
            expansions = location.wishlist_expansions.all()
        else:
            games = location.game.all()
            expansions = location.expansions.all()
    
    if(request.GET.get('genre')):
        games = games.filter(genre__in=request.GET.getlist('genre'))
        expansions = expansions.filter(genre__in=request.GET.getlist('genre'))
    
    if(request.GET.get('player')and int(request.GET.get('player'))!=0):
        player = int(request.GET.get('player'))
        games = games.filter(min_player__lte=player, max_player__gte=player)
        expansions = expansions.filter(min_player__lte=player, max_player__gte=player)
    
    if(request.GET.get('teaming')):
        games = games.filter(teaming__in=request.GET.getlist('teaming'))
        expansions = expansions.filter(teaming__in=request.GET.getlist('teaming'))
    
    if(request.GET.get('duration') and int(request.GET.get('duration'))!=0):
        games = games.filter(duration__lte=int(request.GET.get('duration')))
        expansions = expansions.filter(duration__lte=int(request.GET.get('duration')))
    if location:
        expansionGames = location.game.filter(expansion__in=expansions)
    if expansionGames:
        notGames = expansionGames.exclude(pk__in=games).distinct()
        games = (games|expansionGames)
    if typeValue=="collection":
        games = models.dislikes.objects.filter(game__in=games, location=location)
    else:
        games = games.distinct()
    
    gameData = {}
    gameData["games"] = games
    gameData["notGames"] = notGames
    gameData["expansions"] = expansions

    return gameData

