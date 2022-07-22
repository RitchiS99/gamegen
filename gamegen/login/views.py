from django.db.models.manager import Manager
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import scripts.generator
from home.models import Spiel, Genre, Ort, VS, Rechte
import itertools
import pickle
from django.contrib import auth, messages
from django.shortcuts import render



# from spielegenerator.home.models import Ort

# from spielegenerator.home.models import Genre

# Create your views here.
def index(request, context={}):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('login/index.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        # print("Authenticated")
        # print(user)
        # print(user.ldap_user.group_names)
        # print(user.__dir__())
        if user is not None:
            # correct username and password login the user
            rechtsObjekt = list(Rechte.objects.filter(person=user))
            if not rechtsObjekt:
                rechte = Rechte(person=user)
                rechte.save()
                demoOrt = list(Ort.objects.filter(orte_name="Demo"))
                if demoOrt:
                    demoOrt = demoOrt[0]
                    user.rechte.viewer.add(demoOrt)
            auth.login(request, user)
            return HttpResponseRedirect('/')

        else:
            # messages.error(request, 'Error wrong username/password')
            messages.error(request, 'Error wrong username/password')
            print("Existiert nicht")
    context = {
        'messages'
    }
    return render(request, 'login/index.html')
    return HttpResponse(template.render(context, request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

# def login(request):
#     if request.user.is_authenticated():
#         return redirect('admin_page')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(username=username, password=password)

#         if user is not None:
#             # correct username and password login the user
#             auth.login(request, user)
#             return redirect('admin_page')

#         else:
#             messages.error(request, 'Error wrong username/password')

#     return render(request, 'blog/login.html')