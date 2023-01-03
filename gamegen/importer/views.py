from django.db.models.manager import Manager
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import scripts.generator
from home.models import Erweiterungen, Spiel, Genre, Ort, VS, Zeit, GENRE, TIME, TEAMING
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
            ort = editer + creater
            orte = scripts.generator.ortauswertung(ort)
            auswahl = {"ort":"", "genres": None, "personen": [], "zeiten": None, "versus": None, "spielerzahl":None}
            for ortx in orte:
                auswahl["ort"] = ortx
                gefundenes = scripts.generator.spieleauswertung(auswahl)
                spiele.extend(gefundenes)

    else:
        return HttpResponseRedirect('/login')

    # Now the new Stuff


    genres = GENRE
    versus = TEAMING
    zeiten = TIME
    zeiten = list(reversed(zeiten))
    zeitenlist = []
    for zeit in zeiten:
        zeit_dict = {"label": zeit.label, "name": zeit.name, "value": zeit.value}
        zeitenlist.append(zeit_dict)
    print("Zeiten")
    print(zeitenlist)
    # zeitenlist = json.dumps(zeiten)
    # zeitenlist = zeitenlist.replace('/&#x27;/gm', '"')
    # zeitenlist = json.parse(zeitenlist)
    context = {
        'empty': None,
        'genres': genres,
        'versus': versus,
        'zeiten': zeitenlist,
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME
    }
    return HttpResponse(template.render(context, request))
def saveGame(request, context={}):
    if request.method == 'POST':
        data = request.POST.get("jsonField", "")
        data = json.loads(data)
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
    for i in GENRE:
        if i.name == spiel['genres']:
            genre = i
    for i in TIME:
        if i.name == spiel['time']:
            dauer = i
    for i in TEAMING:
        if i.name == spiel['versus']:
            versus = i
    minSpieler=spiel['minPlayer']
    maxSpieler=spiel['maxPlayer']
    rules = ""
    print("Neues Spiel")
    print(dauer)
    print(versus)
    print(genre)
    spiel = Spiel(name=name, ort=ort, genre=genre, vs=versus, zeit=dauer, minSpieler=minSpieler, maxSpieler=maxSpieler, rules=rules)
    spiel.save()

def updateGame(spielNeu, spielAlt):

    game = spielAlt
    for i in GENRE:
        if i.name == spielNeu['genres']:
            genre = i
    for i in TIME:
        if i.name == spielNeu['time']:
            dauer = i
    for i in TEAMING:
        if i.name == spielNeu['versus']:
            versus = i
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

    