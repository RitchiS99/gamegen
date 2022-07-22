from django.db.models.manager import Manager
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import scripts.generator
from home.models import Spiel, Genre, Ort, VS, Personen, Zeit, Rechte, Erweiterungen
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
    print("User =")

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
    context = {
        'orte': orte,
        'spiele': spiele,
        'WebsiteName': settings.NAME,
        
    }
    if request.method == 'POST':
        werte = request.POST
        if werte.get('methode') == "newOrt":
            # addOrt(werte.get('ortsname'))
            template = loader.get_template('editor/addOrt.html')
        elif werte.get('methode') == "newUser":
            # addOrt(werte.get('ortsname'))
            template = loader.get_template('editor/addUser.html')
        elif werte.get('methode')=="addUser":
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

        elif werte.get('methode')=="EditGame":
            id = werte.get("gameID")
            context = editGame(request, id, orte)
            template = loader.get_template('editor/editGame.html')
        elif werte.get('methode')=="SaveGame":
            saveGame(werte)
        elif werte.get('methode')=="deleteGame":
            id = werte.get('gameID')
            deleteSomething("game", id)
        elif werte.get('methode')=="deleteOrt":
            id = werte.get('ortname')
            deleteSomething("ort", id)
        elif werte.get('methode')=="deleteErweiterung":
            id = werte.get('erweiterungid')
            deleteSomething("erweiterung", id)
            endErweiterung = scripts.generator.erweiterungen(ort)
            context['endErweiterung'] = endErweiterung
            template = loader.get_template('editor/erweiterungVerwaltung.html')
        elif werte.get('methode')=="addOrt":
            ortname = werte.get('ortName')
            print("Ortname")
            print(ortname)
            personenname = werte.get('ortPersonen')
            personenname = personenname.replace(" ", "")
            print(personenname)
            ortList = list(Ort.objects.filter(orte_name=ortname))
            if ortList:
                messages.error(request, _('locationDoesExist'))
                context['personennamen'] = personenname
                context['ortnamen'] = ortname
                print(type(context['personennamen']))
                template = loader.get_template('editor/addOrt.html')
                pass
            else:
                addOrt(request.user, ortname, personenname)
            pass
        elif werte.get('methode')=="ortVerwaltung":
            endOrte = []
            for x in creater:
                einzelnerOrt = {'name':x.orte_name}
                print("Orte Dict")
                personenNachOrt = list(Personen.objects.filter(ort=x))
                print(personenNachOrt)
                personenList = []
                for einzelnePerson in personenNachOrt:
                    print(einzelnePerson)
                    print(einzelnePerson.name)
                    personenList.append(einzelnePerson.name)
                personenString = ",".join(personenList)
                einzelnerOrt['personen'] = personenString
                endOrte.append(einzelnerOrt)
                print("EndOrte")
                print(endOrte)
            context['endOrte'] = endOrte
            template = loader.get_template('editor/ortVerwaltung.html')
        elif werte.get('methode')=="erweiterungVerwaltung":
            endErweiterung = scripts.generator.erweiterungen(ort)
            context['endErweiterung'] = endErweiterung
            template = loader.get_template('editor/erweiterungVerwaltung.html')
        elif werte.get('methode')=="addGame":
            context['personen'] = scripts.generator.ortspersonen(orte)
            context['genres'] = scripts.generator.genre()
            context['vs'] = scripts.generator.vs()
            context['zeiten'] = scripts.generator.zeiten()
            template = loader.get_template('editor/addGame.html')
        elif werte.get('methode')=="addErweiterung":
            ort_ids = []
            alleSpiele = []
            for id in ort:
                spiele = list(Spiel.objects.filter(ort=id))
                alleSpiele.extend(spiele)
            context['grundspiele'] = alleSpiele
            print("Context grundspiele")
            print(context['grundspiele'])
            template = loader.get_template('editor/addErweiterung.html')
        elif werte.get('methode')=="AddingGame":
            ort = werte.get('gameOrt')
            disliker = request.POST.getlist(ort)
            addGame(werte, disliker)
        elif werte.get('methode')=="addingErweiterung":
            addErweiterung(werte)
            endErweiterung = scripts.generator.erweiterungen(ort)
            context['endErweiterung'] = endErweiterung
            template = loader.get_template('editor/erweiterungVerwaltung.html')
        elif werte.get('methode')=="editOrt":
            ortname = werte.get('ortname')
            personen = werte.get('ortpersonen')
            template = loader.get_template('editor/editOrt.html')
            context['ortname'] = ortname
            context['personenNamen'] = personen
        elif werte.get('methode')=="saveEditOrt":
            ortname = werte.get('ortName')
            neuerOrtname = werte.get('ortNameNew')
            personen = werte.get('ortPersonen')
            print("CallEditOrt")
            editOrt(ortname, neuerOrtname, personen)
        elif werte.get('methode')=="personenVerwaltung":
            viewerRechte = list(Rechte.objects.filter(viewer__in=creater))
            editerRechte = list(Rechte.objects.filter(editer__in=creater))
            print(viewerRechte)
            print(editerRechte)

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
                            print("Ist drinnen")
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
                            print("Dicte")
                            print(dicte)
                            volleListe.append(dicte)
            print("Endliste")           
            print(volleListe)
            context['personenVerwaltung'] = volleListe
            # pass
            template = loader.get_template('editor/personenVerwaltung.html')
        elif werte.get('methode')=="deletePerson":
            personName = werte.get('personName')
            person = list(User.objects.filter(username=personName))[0]
            personRolle = werte.get('personRolle')
            personOrt = werte.get('personOrt')
            ort = list(Ort.objects.filter(orte_name=personOrt))[0]
            rechte = list(Rechte.objects.filter(person=person))[0]
            if personRolle == 'Editer':
                rechte.editer.remove(ort)
                pass
            elif personRolle == 'Viewer':
                rechte.viewer.remove(ort)

            pass


        

    
            # orte = scripts.generator.ortauswertung(ort)
            # personen = scripts.generator.ortspersonen(orte)

    # Spiele mit ID übergeben
    
    return HttpResponse(template.render(context, request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def saveGame(id, genre, name, vs, ort, zeit, minSpieler, maxSpieler, dislikes):
    game = Spiel.objects.get(id=id)
    game.genre = genre
    game.name = name
    game.vs = vs
    game.ort = ort
    game.zeit = zeit
    game.minSpieler = minSpieler
    game.maxSpieler = maxSpieler
    game.dislikes = dislikes
    game.save()



def editGame(request, id, orte):
    game = Spiel.objects.get(id = id)
    spiel_dict = game.__dict__
    spiel_dict['genre'] = game.genre.genre_name
    vs_of_game = (VS.objects.get(pk=spiel_dict['vs_id'])).__dict__['versus_name']
    spiel_dict['versus'] = game.vs.versus_name
    spiel_dict['zeit'] = game.zeit.zeit_einteilung
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
    genres = scripts.generator.genre()
    vs = scripts.generator.vs()
    zeiten = scripts.generator.zeiten()
    print("Game")
    print(spiel_dict)
    context = {
        'orte': orte,
        'game': spiel_dict,
        'personen': personen[spiel_dict['ort']],
        'genres': genres,
        'vs': vs,
        'zeiten': zeiten,
        'ort': spiel_dict['ort']
        
    }
    print("Test123")
    return(context)
    return HttpResponse(template.render(context, request))
def saveGame(inhalte):
    game = Spiel.objects.get(id=inhalte.get('gameID'))
    game.name = inhalte.get('gameName')
    game.genre = Genre.objects.get(genre_name=inhalte.get('gameGenre'))
    game.vs = VS.objects.get(versus_name=inhalte.get('gameVersus'))
    game.ort = Ort.objects.get(orte_name=inhalte.get('gameOrt'))
    game.zeit = Zeit.objects.get(zeit_einteilung=inhalte.get('gameDauer'))
    game.minSpieler = inhalte.get('gameMinSpieler')
    game.maxSpieler = inhalte.get('gameMaxSpieler')
    game.rules = inhalte.get('rules')
    game.save()
	# game.dislikes = 
    print(game)
    print("Save Game")
    print(inhalte)
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
            print("Neue Person")
            # print(newPerson)
            newPerson = Personen(name=person)
            newPerson.save()
            newPerson.ort.add(ort)

def addUser(username, mail, rolle, ortname, request):
    print(username)
    userList = list(User.objects.filter(username=username))
    ort = list(Ort.objects.filter(orte_name=ortname))
    ort = ort[0]
    demoOrt = list(Ort.objects.filter(orte_name="Demo"))
    websiteLink = settings.CSRF_TRUSTED_ORIGINS
    registrationMailStart = settings.REGISTRATION_MAIL_TEXT
    #Ort muss noch hinzugefügt werden
    
    if userList:
        user = userList[0]
        print(user.__dict__)
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
    print("Nutzer")
    if rolle=="Viewer":
        print("User Rechte Viewer")
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

def deleteSomething(art, id):
    if art == "game":
        game = Spiel.objects.get(id = id)
        game.delete()
    if art == "erweiterung":
        erweiterung = Erweiterungen.objects.get(id=id)
        erweiterung.delete()
    if art == "ort":
        ort = Ort.objects.get(orte_name=id)
        ort.delete()
def addGame(werte, disliker):
    name = werte['gameName']
    ortName=werte['gameOrt']
    ort=Ort.objects.get(orte_name=ortName)
    genreName=werte['gameGenre']
    genre=Genre.objects.get(genre_name=genreName)
    versusName=werte['gameVersus']
    versus=VS.objects.get(versus_name=versusName)
    dauerName=werte['gameDauer']
    dauer=Zeit.objects.get(zeit_einteilung=dauerName)
    minSpieler=werte['gameMinSpieler']
    maxSpieler=werte['gameMaxSpieler']
    rules = werte['rules']
    
    spiel = Spiel(name=name, ort=ort, genre=genre, vs=versus, zeit=dauer, minSpieler=minSpieler, maxSpieler=maxSpieler, rules=rules)
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
    print("OrtDict")
    print(ort.__dict__)
    print(ort)
    print(filterPersonen)
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
            print("Neue Person")
            # print(newPerson)
            newPerson = Personen(name=person)
            newPerson.save()
            newPerson.ort.add(ort)
    
def addErweiterung(werte):
    name = werte['erweiterungName']
    nummer=werte['erweiterungNummer']
    grundspiel_id=werte['erweiterungGrundspiel']
    minSpieler=werte['erweiterungMin']
    maxSpieler=werte['erweiterungMax']
    print("get grundspiel")
    grundspiel = Spiel.objects.get(pk=grundspiel_id)
    print("Grundspiel ist: ")
    print(grundspiel)
    erweiterung = Erweiterungen(name=name, grundspiel=grundspiel, minSpieler=minSpieler, maxSpieler=maxSpieler, nummer=nummer)
    erweiterung.save()