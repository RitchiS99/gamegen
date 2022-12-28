from django.db.models.manager import Manager
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import scripts.generator
from home.models import Spiel, Genre, Ort, VS
import itertools
import pickle
import random
import json
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import gettext as _

# from spielegenerator.home.models import Ort

# from spielegenerator.home.models import Genre

# Create your views here.
def index(request, context={}):
    template = loader.get_template('home/index.html')
    ort = list(Ort.objects.all())
    orte = scripts.generator.ortauswertung(ort)
    personen = scripts.generator.ortspersonen(orte)
    genres = scripts.generator.genre()
    vs = scripts.generator.vs()
    zeiten = scripts.generator.zeiten()
    auswahl = {"ort":"", "genres": "", "personen": [], "zeiten": "", "versus": "", "spielerzahl":""}
    erstesBeispiel = {}
    gefundenes = []
    genre = Genre.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            pass
        else:
            user = request.user.rechte
            viewer = list(user.viewer.all())
            editer = list(user.editer.all())
            creater = list(user.creater.all())
            print(viewer)
            print(editer)
            print(creater)
            ort = editer + creater +viewer
            orte = scripts.generator.ortauswertung(ort)
            personen = scripts.generator.ortspersonen(orte)
    else:
        ort = list(Ort.objects.all().filter(orte_name="Demo"))
        orte = scripts.generator.ortauswertung(ort)
        personen = scripts.generator.ortspersonen(orte)
    

    if request.method == 'POST':
        ort = request.POST.get('ort')
        genre = request.POST.get('genre')
        spielerzahl = request.POST.get('spielerzahl')
        versus = request.POST.get('versus')
        zeit = request.POST.get('zeit')
        dislike = request.POST.getlist(ort)

        if (spielerzahl==""):
            spielerzahl=None

        auswahl['ort']=ort
        auswahl['genres']=genre
        auswahl['zeiten']=zeit
        auswahl['versus']=versus
        auswahl['spielerzahl']=spielerzahl
        auswahl['personen'] = dislike
        print("Auswahl")
        print(auswahl)
        gefundenes = scripts.generator.spieleauswertung(auswahl)
        print("Gefundenes ist ")
        extensionString = _('extensionString')
        playerString = _('playerString')
        for i in gefundenes:
            if i['erweiterungen']:
                print("i von erweiterungen")
                print(i['erweiterungen'])
                i['erweiterungen'] = i['erweiterungen'].replace(". Erweiterung", extensionString)
                i['erweiterungen'] = i['erweiterungen'].replace(" Spieler)", playerString)

    context = {
        'orte': orte,
        'personen': personen,
        'genres': genres,
        'zeiten': zeiten,
        'vs': vs,
        'auswahl': auswahl,
        'gefundenes': gefundenes,
        'WebsiteName': settings.NAME
    }
    return HttpResponse(template.render(context, request))

def alexa(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            print(request.GET)
            location=""
            genre="None"
            time="None"
            versus="None"
            count="None"
            if "location" in request.GET:
                location = request.GET["location"]
            if "genre" in request.GET:
                genre = request.GET["genre"]
            if "time" in request.GET:
                time = request.GET["time"]
            if "versus" in request.GET:
                versus = request.GET["versus"]
            if "count" in request.GET:
                if "count" == 0:
                    count = request.GET["count"]
            selection = {"ort": location, "genres": genre, "zeiten": time, "versus": versus, "spielerzahl": count, "personen": []}
            print(selection)
            foundedGames = scripts.generator.spieleauswertung(selection)
            print(foundedGames)
            game_count = len(foundedGames)
            
            if game_count >=3:
                random_int = 3
            else:
                random_int = game_count
            random_games = random.sample(foundedGames, random_int)
            name_list = []
            print("Name List")
            for i in random_games:
                name_list.append(i["name"])
                print(name_list)
            data = json.dumps(name_list, separators=(',', ':'))
            response = JsonResponse(data, safe=False)
            response = HttpResponse(data)
            return response



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def change_password(request):
    if request.user.is_authenticated:
        if 'ldap_user' in request.user.__dir__():
            LDAP_PASSWORD_CHANGE_LINK = settings.LDAP_CHANGE_PASSWORD
            # return HttpResponseRedirect('https://manager.richardschoebel.de/user/password/reset/')
            return HttpResponseRedirect(LDAP_PASSWORD_CHANGE_LINK)

        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                return redirect('change_password')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'home/change_password.html', {
            'form': form
        })
    else:
        return redirect("/login")