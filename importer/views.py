from django.db.models.manager import Manager
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import scripts.generator
from home.models import Erweiterungen, Spiel, Genre, Ort, VS, Zeit
import itertools
import pickle
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import gettext as _
import json

# Create your views here.
def index(request, context={}):
    template = loader.get_template('importer/index.html')
    
    # Find Creater and Editor
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
            print("Superuser")
            print(orte)
            auswahl = {"ort":"", "genres": None, "personen": [], "zeiten": None, "versus": None, "spielerzahl":None}
            for ortx in orte:
                auswahl["ort"] = ortx
                gefundenes = scripts.generator.spieleauswertung(auswahl)
                spiele.extend(gefundenes)
                pass
        else:
            user = request.user.rechte
            viewer = list(user.viewer.all())
            editer = list(user.editer.all())
            creater = list(user.creater.all())
            print(viewer)
            print(editer)
            print(creater)
            ort = editer + creater
            orte = scripts.generator.ortauswertung(ort)
            print("orte")
            print(orte)
            auswahl = {"ort":"", "genres": None, "personen": [], "zeiten": None, "versus": None, "spielerzahl":None}
            for ortx in orte:
                auswahl["ort"] = ortx
                print(auswahl)
                gefundenes = scripts.generator.spieleauswertung(auswahl)
                spiele.extend(gefundenes)

    else:
        return HttpResponseRedirect('/login')

    # Now the new Stuff


    genres = scripts.generator.genre()
    versus = scripts.generator.vs()
    zeiten = list(Zeit.objects.all())
    print("Zeiten sind ")
    print(zeiten[0].__dir__())
    context = {
        'empty': None,
        'genres': genres,
        'versus': versus,
        'zeiten': zeiten,
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME
    }
    return HttpResponse(template.render(context, request))
def saveGame(request, context={}):
    data = request.POST.get("jsonField", "")
    data = json.loads(data)
    print(type(data))
    print(data)
    ort = data["ort"]
    ortModel = Ort.objects.get(orte_name=ort)
    overwrite = data['overwrite']
    basegames = data['basegames']
    expansions = data['expansion']
    for game in basegames:
        spiel = Spiel.objects.filter(ort=ortModel, name=game['name'])
        if spiel:
            if overwrite:
                einzelnesSpiel = spiel[0]
                updateGame(game, einzelnesSpiel)
        else:
            addGame(game, ortModel)
    for expansion in expansions:
        grundspiel = Spiel.objects.get(ort=ortModel, name=expansion['basegame'])
        # erweiterung = Erweiterungen.objects.filter(grundspiel=grundspiel, name=expansion['name'])
        erweiterung = Erweiterungen.objects.filter(grundspiel__ort=ortModel, name=expansion['name'])
        if erweiterung:
            if overwrite:
                einzelneErweiterung = erweiterung[0]
                updateErweiterung(expansion, einzelneErweiterung,grundspiel)
        else:
            addErweiterung(expansion, grundspiel)


    return HttpResponseRedirect('/')



    



def addGame(spiel, ort):
    name = spiel['name']
    ort=ort
    genre=Genre.objects.get(genre_name=spiel['genre'])
    versus=VS.objects.get(versus_name=spiel['versus'])
    dauer=Zeit.objects.get(zeit_einteilung=spiel['time'])
    minSpieler=spiel['minPlayer']
    maxSpieler=spiel['maxPlayer']
    rules = ""
    spiel = Spiel(name=name, ort=ort, genre=genre, vs=versus, zeit=dauer, minSpieler=minSpieler, maxSpieler=maxSpieler, rules=rules)
    spiel.save()

def updateGame(spielNeu, spielAlt):

    game = spielAlt
    game.genre = Genre.objects.get(genre_name=spielNeu['genre'])
    game.vs = VS.objects.get(versus_name=spielNeu['versus'])
    game.zeit = Zeit.objects.get(zeit_einteilung=spielNeu['time'])
    game.minSpieler = spielNeu['minPlayer']
    game.maxSpieler = spielNeu['maxPlayer']
    game.save()

def addErweiterung(erweiterung, grundspiel):
    name = erweiterung['name']
    nummer=erweiterung['number']
    minSpieler=erweiterung['minPlayer']
    maxSpieler=erweiterung['maxPlayer']
    extension = Erweiterungen(name=name, grundspiel=grundspiel, minSpieler=minSpieler, maxSpieler=maxSpieler, nummer=nummer)
    extension.save()



def updateErweiterung(erweiterung, erweiterungAlt, grundspiel):
    extension = erweiterungAlt
    extension.nummer = erweiterung['number']
    extension.minSpieler = erweiterung['minPlayer']
    extension.maxSpieler = erweiterung['maxPlayer']
    extension.grundspiel = grundspiel
    extension.save()

    