from django.db.models.manager import Manager
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import scripts.generator
from home.models import Spiel, Genre, Ort, VS, Personen, Zeit, Rechte, Erweiterungen, GENRE, TIME, TEAMING
import itertools
import pickle
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission, User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# from spielegenerator.home.models import Ort

# from spielegenerator.home.models import Genre

# Create your views here.
def index(request, context={}):
    template = loader.get_template('editor/index.html')
    orte = []
    spiele = []

    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
            auswahl = {"ort":"", "genres": "None", "personen": [], "zeiten": "None", "versus": "None", "spielerzahl":None}
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
            auswahl = {"ort":"", "genres": "None", "personen": [], "zeiten": "None", "versus": "None", "spielerzahl":None}
            for ortx in orte:
                auswahl["ort"] = ortx
                gefundenes = scripts.generator.spieleauswertung(auswahl)
                spiele.extend(gefundenes)

    else:
        return HttpResponseRedirect('/login')
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }


    
    return HttpResponse(template.render(context, request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')




def editGame(request, id, orte):
    game = Spiel.objects.get(id = id)
    spiel_dict = game.__dict__
    for i in GENRE:
        if i.value == game.group:
            spiel_dict['genre'] = i
    for i in TEAMING:
        if i.value == game.teaming:
            spiel_dict['versus'] = i
    for i in TIME:
        if i.value == game.time:
            spiel_dict['zeit'] = i
    spiel_dict['ort'] = game.ort.orte_name
    spiel_dict['id'] = game.id
    spiel_dict['rules'] = game.rules
    dislikes = list(game.dislikes.all())
    disliker = []
    for dislike in dislikes:
        disliker.append(dislike.name)
        # Hier weiter
    spiel_dict['Personen'] = disliker


    personen = scripts.generator.ortspersonen(orte)
    genres = GENRE
    vs = TEAMING
    zeiten = TIME
    context = {
        'orte': orte,
        'game': spiel_dict,
        'personen': personen[spiel_dict['ort']],
        'genres': genres,
        'vs': vs,
        'zeiten': zeiten,
        'ort': spiel_dict['ort']
        
    }
    return(context)
def editExtension(request, id, orte):
    extension = Erweiterungen.objects.get(id = id)
    extension_dict = extension.__dict__
    basegame = (Spiel.objects.get(pk=extension_dict['grundspiel_id']))
    extension_dict['basegame'] = basegame
        # Hier weiter


    personen = scripts.generator.ortspersonen(orte)
    genres = scripts.generator.genre()
    vs = scripts.generator.vs()
    zeiten = scripts.generator.zeiten()
    context = {
        'orte': orte,
        'extension': extension_dict,
        'basegame': extension_dict['basegame'],
        'basegame_ort': basegame.ort.orte_name,
        
    }
    return(context)
def saveGame(inhalte):
    game = Spiel.objects.get(id=inhalte.get('gameID'))
    game.name = inhalte.get('gameName')
    for i in GENRE:
        if i.name == inhalte.get('gameGenre'):
            game.group = i
    for i in TEAMING:
        if i.name == inhalte.get('gameVersus'):
            game.teaming = i
    for i in TIME:
        if i.name == inhalte.get('gameDauer'):
            game.time = i
    game.ort = Ort.objects.get(orte_name=inhalte.get('gameOrt'))
    game.minSpieler = inhalte.get('gameMinSpieler')
    game.maxSpieler = inhalte.get('gameMaxSpieler')
    game.rules = inhalte.get('rules')
    game.save()
def saveExtension(inhalte):
    extension = Erweiterungen.objects.get(id=inhalte.get('extensionID'))
    extension.name = inhalte.get('erweiterungName')
    extension.nummer = inhalte.get('erweiterungNummer')
    extension.grundspiel = Spiel.objects.get(id=inhalte.get('erweiterungGrundspiel'))
    extension.minSpieler = inhalte.get('erweiterungMin')
    extension.maxSpieler = inhalte.get('erweiterungMax')
    extension.save()
def addOrt(user, ortname, personen):
    ort = Ort(orte_name=ortname)
    ort.save()
    user.rechte.creater.add(ort)
    user.save()
    personenList = personen.split(',')
    gefundenePersonen = []
    allePersonen = list(Personen.objects.all())
    for person in personenList:
        for name in allePersonen:
            if name.name == person:
                name.ort.add(ort)
                gefundenePersonen.append(person)
    for person in personenList:
        if person not in gefundenePersonen:
            newPerson = Personen(name=person)
            newPerson.save()
            newPerson.ort.add(ort)

def addUser(username, mail, rolle, ortname, request):
    userList = list(User.objects.filter(username=username))
    ort = list(Ort.objects.filter(orte_name=ortname))
    ort = ort[0]
    demoOrt = list(Ort.objects.filter(orte_name="Demo"))
    websiteLink = settings.CSRF_TRUSTED_ORIGINS
    registrationMailStart = settings.REGISTRATION_MAIL_TEXT
    #Ort muss noch hinzugefügt werden
    
    if userList:
        user = userList[0]
    else:
        unencryptedPassword = User.objects.make_random_password()
        passwort = make_password(unencryptedPassword)
        user = User(username=username, password=passwort, email=mail)
        yourUsernameIs = _('yourUsernameIs')
        yourPasswordIs = _('yourPasswordIs')
        changePassword = _('changePassword')
        user.save()
            #send Mail to user
        mail_text = registrationMailStart + "\n\n" +yourUsernameIs +username+ "\n\n"+ yourPasswordIs+ unencryptedPassword + "\n\n" + changePassword + websiteLink[0]
        send_mail('Registrierung bei '+ websiteLink[0], mail_text,from_email=settings.EMAIL_HOST_USER, recipient_list=[mail], fail_silently=False)
        rechte = Rechte(person=user)
        rechte.save()
    if rolle=="Viewer":
        userList = list(user.rechte.viewer.all())
        user.rechte.viewer.add(ort)

    else:
        userList = list(user.rechte.editer.all())
        
        user.rechte.editer.add(ort)
    try:
        demoOrt = demoOrt[0]
        user.rechte.viewer.add(demoOrt)
    except:
        print("Demoort existiert nicht")

    pass


def addGame(werte, disliker):
    for i in GENRE:
        if i.name == werte['gameGenre']:
            genre = i
    for i in TIME:
        if i.name == werte['gameDauer']:
            dauer = i
    for i in TEAMING:
        if i.name == werte['gameVersus']:
            versus = i
    name = werte['gameName']
    ortName=werte['gameOrt']
    ort=Ort.objects.get(orte_name=ortName)
    minSpieler=werte['gameMinSpieler']
    maxSpieler=werte['gameMaxSpieler']
    rules = werte['rules']
    
    spiel = Spiel(name=name, ort=ort, group=genre, teaming=versus, time=dauer, minSpieler=minSpieler, maxSpieler=maxSpieler, rules=rules)
    spiel.save()
    dislikeList = disliker
    if dislikeList:
        for dislike in dislikeList:
            person = Personen.objects.get(name=dislike)
            spiel.dislikes.add(person)

def editOrt(ortnameAlt, ortnameNew, personen):
    ort = list(Ort.objects.filter(orte_name=ortnameAlt))[0]
    ortNew = list(Ort.objects.filter(orte_name=ortnameNew))
    if not ortNew:
        ort.orte_name = ortnameNew
    else:
        pass
    personen = personen.replace(" ", "")
    personenList = personen.split(',')
    gefundenePersonen = []
    allePersonen = list(Personen.objects.all())
    filterPersonen = list(Personen.objects.filter(ort=ort))
    for person in filterPersonen:
        perso = Personen.objects.get(name=person)
        perso.ort.remove(ort)
    ort.save()
    for person in personenList:
        for name in allePersonen:
            if name.name == person:
                name.ort.add(ort)
                gefundenePersonen.append(person)
    for person in personenList:
        if person not in gefundenePersonen:
            newPerson = Personen(name=person)
            newPerson.save()
            newPerson.ort.add(ort)
    
def addErweiterung(werte):
    name = werte['erweiterungName']
    nummer=werte['erweiterungNummer']
    grundspiel_id=werte['erweiterungGrundspiel']
    minSpieler=werte['erweiterungMin']
    maxSpieler=werte['erweiterungMax']
    grundspiel = Spiel.objects.get(pk=grundspiel_id)
    erweiterung = Erweiterungen(name=name, grundspiel=grundspiel, minSpieler=minSpieler, maxSpieler=maxSpieler, nummer=nummer)
    erweiterung.save()

def overview_location(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    endOrte = []
    for x in creater:
        einzelnerOrt = {'name':x.orte_name}
        personenNachOrt = list(Personen.objects.filter(ort=x))
        personenList = []
        for einzelnePerson in personenNachOrt:
            personenList.append(einzelnePerson.name)
        personenString = ",".join(personenList)
        einzelnerOrt['personen'] = personenString
        endOrte.append(einzelnerOrt)
    context['endOrte'] = endOrte
    template = loader.get_template('editor/ortVerwaltung.html')
    return HttpResponse(template.render(context, request))
    pass
def edit_location(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "POST":
        werte = request.POST
        ortname = werte.get('ortName')
        neuerOrtname = werte.get('ortNameNew')
        personen = werte.get('ortPersonen')
        editOrt(ortname, neuerOrtname, personen)
        pass
    elif request.method == "GET":
        if "l" in request.GET:
            ort_name = str(request.GET["l"])
        ort = Ort.objects.get(orte_name = ort_name)
        if ort.orte_name in orte:
            personenOrt = list(Personen.objects.filter(ort=ort))
            ortsperson = []
            for einzelnePerson in personenOrt:
                ortsperson.append(einzelnePerson.name)
            context['ortname'] = ort.orte_name
            context['personenNamen'] = ",".join(ortsperson)
            template = loader.get_template('editor/editOrt.html')
            return HttpResponse(template.render(context, request))

    ####
    return HttpResponseRedirect('/editor/location')
def delete_location(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "GET":
        if "l" in request.GET:
            ort_id = str(request.GET["l"])
            ort = Ort.objects.get(orte_name=ort_id)
            if ort.orte_name in orte:
                if ort in creater:
                    ort.delete()
    return HttpResponseRedirect('/editor/location')
    pass
def add_location(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "POST":
        werte = request.POST
        ortname = werte.get('ortName')
        personenname = werte.get('ortPersonen')
        personenname = personenname.replace(" ", "")
        ortList = list(Ort.objects.filter(orte_name=ortname))
        if ortList:
            messages.error(request, _('locationDoesExist'))
            context['personennamen'] = personenname
            context['ortnamen'] = ortname
            template = loader.get_template('editor/addOrt.html')
        else:
            addOrt(request.user, ortname, personenname)
    else:
        template = loader.get_template('editor/addOrt.html')
        return HttpResponse(template.render(context, request))
    return HttpResponseRedirect('/editor/location')

def overview_user(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    viewerRechte = list(Rechte.objects.filter(viewer__in=creater))
    editerRechte = list(Rechte.objects.filter(editer__in=creater))

    volleListe = []
    viewerListe = []
    for viewPerson in viewerRechte:
        personenName = viewPerson.person
        ortRechte = list(viewPerson.viewer.all())
        dicte = {}
        for orti in ortRechte:
            if orti in creater:
                dicte={}
                dicte['person'] = personenName.username
                dicte['rolle'] = "Viewer"
                dicte['ort'] = orti.orte_name
                if dicte in volleListe:
                    pass
                else:
                    volleListe.append(dicte)

    editerListe =[]
    for editerPerson in editerRechte:
        personenName = editerPerson.person
        ortRechte = list(editerPerson.editer.all())
        dicte = {}
        for orti in ortRechte:

            if orti in creater:
                dicte = {}
                dicte['person'] = personenName.username
                dicte['rolle'] = "Editer"
                dicte['ort'] = orti.orte_name
                if dicte in volleListe:
                    pass
                else:
                    volleListe.append(dicte)
    context['personenVerwaltung'] = volleListe
    # pass
    template = loader.get_template('editor/personenVerwaltung.html')
    return HttpResponse(template.render(context, request))
        
def delete_user(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "GET":
        if "p" in request.GET and "r" in request.GET and "l" in request.GET:
            name_id = str(request.GET["p"])
            person = list(User.objects.filter(username=name_id))[0]
            personRolle = str(request.GET["r"])
            personOrt = str(request.GET["l"])
            ort = list(Ort.objects.filter(orte_name=personOrt))[0]
            rechte = list(Rechte.objects.filter(person=person))[0]
            if ort in creater:
                if personRolle == 'Editer':
                    rechte.editer.remove(ort)
                    pass
                elif personRolle == 'Viewer':
                    rechte.viewer.remove(ort)
                pass
    return HttpResponseRedirect('/editor/user')
    
def add_user(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == 'POST':
        werte = request.POST
        username = werte.get("userName")
        mail = werte.get("userMail")
        rolle = werte.get("userRole")
        userOrt = werte.get("userOrt")
        userList = list(User.objects.filter(username=username))
        if not userList:
            if not mail:
                messages.error(request, _('userDoesntExist'))
                context['username'] = username
                context['userOrt'] = userOrt
                context['rolle'] = rolle
                template = loader.get_template('editor/addUser.html')
            else:
                addUser(username, mail, rolle, userOrt, request)
        else:
            addUser(username, mail, rolle, userOrt, request)
        return HttpResponseRedirect('/editor/user')

    template = loader.get_template('editor/addUser.html')
    return HttpResponse(template.render(context, request))
    pass

def overview_extension(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    endErweiterung = scripts.generator.erweiterungen(ort)
    context['endErweiterung'] = endErweiterung
    template = loader.get_template('editor/erweiterungVerwaltung.html')
    return HttpResponse(template.render(context, request))
def add_extension(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == 'POST':
        werte = request.POST
        addErweiterung(werte)
        endErweiterung = scripts.generator.erweiterungen(ort)
        context['endErweiterung'] = endErweiterung
        template = loader.get_template('editor/erweiterungVerwaltung.html')
        return HttpResponseRedirect('/editor/extension')
    ort_ids = []
    alleSpiele = []
    for id in ort:
        spiele = list(Spiel.objects.filter(ort=id))
        alleSpiele.extend(spiele)
    context['grundspiele'] = alleSpiele
    template = loader.get_template('editor/addErweiterung.html')
    return HttpResponse(template.render(context, request))
    pass
def delete_extension(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "GET":
        if "e" in request.GET:
            extension_id = int(request.GET["e"])
            erweiterung = Erweiterungen.objects.get(id=extension_id)
            erweiterung.delete()
    return HttpResponseRedirect("/editor/extension")
    pass
def edit_extension(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "GET":
        if "e" in request.GET:
            extension_id = int(request.GET["e"])
        extension = Erweiterungen.objects.get(id = extension_id)
        if extension.grundspiel.ort.orte_name in orte:
            context = editExtension(request, extension_id, orte)
            alleSpiele = []
            for id in ort:
                spiele = list(Spiel.objects.filter(ort=id))
                alleSpiele.extend(spiele)
            context['grundspiele'] = alleSpiele
            template = loader.get_template('editor/editErweiterung.html')
            return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        werte = request.POST
        saveExtension(werte)
    return HttpResponseRedirect('/editor/extension')

def add_game(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == 'POST':
        werte = request.POST
        ort = werte.get('gameOrt')
        disliker = request.POST.getlist(ort)
        addGame(werte, disliker)
        return HttpResponseRedirect('/editor')
        pass
    else:
        context['personen'] = scripts.generator.ortspersonen(orte)
        context['genres'] = GENRE
        context['vs'] = TEAMING
        context['zeiten'] = TIME
        template = loader.get_template('editor/addGame.html')
        return HttpResponse(template.render(context, request))
    return HttpResponseRedirect('/editor')
    pass
def edit_game(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "GET":
        if "g" in request.GET:
            game_id = int(request.GET["g"])
        game = Spiel.objects.get(id = game_id)
        if game.ort.orte_name in orte:
            context = editGame(request, game_id, orte)
            template = loader.get_template('editor/editGame.html')
            return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        werte = request.POST
        saveGame(werte)
    return HttpResponseRedirect('/editor')
    pass
def delete_game(request):
    orte = []
    spiele = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            ort = list(Ort.objects.all())
            orte = scripts.generator.ortauswertung(ort)
            creater = ort
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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == "GET":
        if "g" in request.GET:
            game_id = int(request.GET["g"])
            game = Spiel.objects.get(id = game_id)
            if game.ort.orte_name in orte:
                game.delete()
    return HttpResponseRedirect('/editor')

    pass


