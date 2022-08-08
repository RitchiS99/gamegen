"""smarthome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views
import scripts.generator
import itertools

urlpatterns = [
    path('', views.index, name='index'),
    path('location', views.overview_location, name="overviewLocation"),
    path('location/add', views.add_location, name="addLocation"),
    path('location/delete', views.delete_location, name="deleteLocation"),
    path('location/edit', views.edit_location, name="editLocation"),
    path('user', views.overview_user, name="overviewUser"),
    path('user/add', views.add_user, name="addUser"),
    path('user/delete', views.delete_user, name="deleteUser"),
    path('extension', views.overview_extension, name="overviewExtension"),
    path('extension/add', views.add_extension, name="addExtension"),
    path('extension/delete', views.delete_extension, name="deleteExtension"),
    path('extension/edit', views.edit_extension, name="editExtension"),
    path('game/add', views.add_game, name="addGame"),
    path('game/delete', views.delete_game, name="deleteGame"),
    path('game/edit', views.edit_game, name="editGame"),
]
