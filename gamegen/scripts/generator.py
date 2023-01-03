import json
import codecs
from home.models import Spiel, Genre, Ort, VS, Personen, Zeit, Erweiterungen, GENRE, TIME, TEAMING



def ortauswertung(ort):
    #ort = list(Ort.objects.all())
    orte = []
    for i in ort:
        orte.append(i.orte_name)
    return orte

def erweiterungen(orte):
    erweiterungsList = []
    erweiterungsDictList = []
    for ort in orte:
        erweiterungen = list(Erweiterungen.objects.filter(grundspiel__ort = ort))
        erweiterungsList.extend(erweiterungen)
    return erweiterungsList
    pass

def ortspersonen(orte):
    #orte = ortauswertung()
    person_ort = {}
    for ort in orte:
        orter = (Ort.objects.filter(orte_name= ort)[:1][0]).id
        personen = list(Personen.objects.filter(ort=orter))
        person = []
        for persone in personen:
            person.append(persone.name)
        person_ort[ort] = person
    return person_ort
# def genre():
#     genr = list(Genre.objects.all())
#     genre = []
#     for i in genr:
#         genre.append(i.genre_name)
#     return genre

# def zeiten():
#     zeit = list(Zeit.objects.all())
#     zeiten = []
#     for i in zeit:
#         zeiten.append(i.zeit_einteilung)
#     return zeiten

# def vs():
#     versus = list(VS.objects.all())
#     vs = []
#     for i in versus:
#         vs.append(i.versus_name)
#     return vs

def spieleauswertung(suche):
    orte_nam = Ort.objects.filter(orte_name= suche['ort'])[:1]
    stade_list = Spiel.objects.filter(ort=orte_nam)
    name = None
    if(suche['genres'] != "None"):
        art = suche['genres']
        stade_list = stade_list.filter(group=suche['genres'])
    else:
        art = None
    
    if(suche['versus'] != "None"):
        vs = suche['versus']
        stade_list = stade_list.filter(teaming=suche['versus'])
    else:
        vs = None
    min = None
    max = None
    if(suche['spielerzahl'] != "None"):
        spielerzahl = suche['spielerzahl']
    else:
        spielerzahl = None
    if(suche['zeiten'] != "None"):
        zeit = suche['zeiten']
        stade_list = stade_list.filter(time=suche['zeiten'])
    else:
        zeit = None
    personen = suche['personen']
    stade_list = list(stade_list)

    bedingungen = {"spiel": name, "Spielerzahl": spielerzahl, "Personen": personen}
    print("Bedingungen")
    print(bedingungen)
    print(stade_list)
    spieleauswahl = []

    for spieles in stade_list:
        spiel_dict = spieles.__dict__
        spiel_dict['genre'] = spieles.group
        spiel_dict['versus'] = spieles.teaming
        spiel_dict['zeit'] = spieles.time
        for i in GENRE:
            if i.value == spieles.group:
                spiel_dict['genre'] = i
        for i in TEAMING:
            if i.value == spieles.teaming:
                spiel_dict['versus'] = i
        for i in TIME:
            if i.value == spieles.time:
                spiel_dict['zeit'] = i
        spiel_dict['ort'] = spieles.ort.orte_name
        spiel_dict['id'] = spieles.id
        erweiterungsList = list(spieles.erweiterungen_set.all())
        erweiterungsList.sort(key=lambda x: x.nummer, reverse=False)
        erweiterungsStringList = []
        spiel_dict["minSpielerErw"] = spiel_dict["minSpieler"]
        spiel_dict["maxSpielerErw"] = spiel_dict["maxSpieler"]
        for erweiterung in erweiterungsList:
            string = erweiterung.name + " - "+str(erweiterung.nummer) + ". Erweiterung " + "(" + str(erweiterung.minSpieler) + "-" + str(erweiterung.maxSpieler) + " Spieler)"
            erweiterungsStringList.append(string)
            if spiel_dict["minSpielerErw"]>erweiterung.minSpieler:
                spiel_dict["minSpielerErw"] = erweiterung.minSpieler
            if spiel_dict["maxSpielerErw"]<erweiterung.maxSpieler:
                spiel_dict["maxSpielerErw"] = erweiterung.maxSpieler
        spiel_dict['erweiterungen'] = ',\n'.join(erweiterungsStringList)
        spiel_dict['namenid'] = "hidden_" + str(spiel_dict['id'])
        dislikes = list(spieles.dislikes.all())
        disliker = []
        for dislike in dislikes:
            disliker.append(dislike.name)
        # Hier weiter
        spiel_dict['Personen'] = disliker
        spiel_dict['personen_string'] = ', '.join(disliker)
        regeln = spieles.rules
        rules = '_.,._'.join(regeln.splitlines())
        spiel_dict['rules'] = rules


        spiel = spiel_dict
        spiel["erwAktiv"] = False
        drinnen = True
        for x in bedingungen.keys():
            if(x == "Spielerzahl" and bedingungen[x] != None):
                if (int(spiel["minSpieler"]) <= int(bedingungen[x]) and int(spiel["maxSpieler"]) >= int(bedingungen[x])):
                    pass
                elif (int(spiel["minSpielerErw"]) <= int(bedingungen[x]) and int(spiel["maxSpielerErw"]) >= int(bedingungen[x])):
                    spiel["minSpieler"] = spiel["minSpielerErw"]
                    spiel["maxSpieler"] = spiel["maxSpielerErw"]
                    spiel["erwAktiv"] = True
                    pass
                else:
                    drinnen = False
                    break
            elif(x == "Personen" ):
                if(bedingungen[x] !=[]  and ("Personen" in spiel.keys())):
                    personen = spiel["Personen"]
                    for spieler in bedingungen[x]:
                        for hater in personen:
                            if(hater == spieler):
                                drinnen = False
                                break
                            else:
                                pass
                else:
                    pass
            elif(((bedingungen[x]==None) or (bedingungen[x] == spiel[x]))):
                pass
            else:
                drinnen=False
                break
        if (drinnen == True):
            spieleauswahl.append(spiel)
    return spieleauswahl

    
