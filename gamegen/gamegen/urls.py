"""
gamegen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views, settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from rest_framework import serializers, generics, permissions
from modelclasses import models

from home.views import filterGames

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.location
        fields = ('name', 'id', 'disliker',)
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.genre
        fields = ('name', 'id',)
class TeamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.teaming
        fields = ('name', 'id',)
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.game
        fields = ('name', 'genre', 'teaming', 'duration', 'min_player', 'max_player',)


class LocationList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = models.location.objects.all()
        else:
            queryset = self.request.user.creater.all()|self.request.user.editer.all()|self.request.user.viewer.all()
        return queryset
    serializer_class = LocationSerializer

class GenreList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.genre.objects.all()
    serializer_class = GenreSerializer

class TeamingList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.teaming.objects.all()
    serializer_class = TeamingSerializer

class GameList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        gameData = filterGames(self.request)
        games = gameData["games"]
        if games.model is models.dislikes:
            allGames = []
            for game in games:
                allGames.append(game.game.id)
            games = models.game.objects.filter(id__in=allGames)
        return games
    serializer_class = GameSerializer






urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('modelclasses/', include('modelclasses.urls')),
    path('', include('home.urls')),
    # path('htmx/', views.htmx_home, name='htmx'),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/location/', LocationList.as_view()),
    path('api/genre/', GenreList.as_view()),
    path('api/teaming/', TeamingList.as_view()),
    path('api/games/', GameList.as_view()),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)