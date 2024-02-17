from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
# from . import htmx


router = routers.DefaultRouter()

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path('', views.HomeView.as_view(), name="HomeView"),
    path('gameTable/', views.gameTable, name="GameTable"),
    path('createGame/', views.CreateGameView.as_view(), name="CreateGameView"),
    path('addDislikes/', views.addDislikes, name="AddDislikes"),
    path('getBGG/', views.loadFromBGG, name="getBGGData"),
    path('saveNewGame/', views.saveNewGame, name="saveNewGame"),
    path('addGame/', views.addGame, name="addGame"),
    path('createExpansion/', views.CreateExpansionView.as_view(), name="CreateExpansionView"),
    path('addWishlist/', views.addWishlist, name="addWishlist"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('changeDislikes', views.changeDislikes, name="changeDislikes"),
    path('changeDislikesSave', views.changeDislikesSave, name="changeDislikesSave"),
    path('addToStorage', views.addToStorage, name="addToStorage"),
    path('deleteElement', views.deleteItem, name="deleteElement"),
    path('settings/', views.UserSettings.as_view(), name="UserSettings"),
)
