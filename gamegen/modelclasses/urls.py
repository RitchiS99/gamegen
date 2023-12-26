from django.urls import path, include
from rest_framework import routers

from . import api
from . import views
from . import htmx


router = routers.DefaultRouter()
router.register("dislikes", api.dislikesViewSet)
router.register("expansion", api.expansionViewSet)
router.register("game", api.gameViewSet)
router.register("genre", api.genreViewSet)
router.register("location", api.locationViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("modelclasses/dislikes/", views.dislikesListView.as_view(), name="modelclasses_dislikes_list"),
    path("modelclasses/dislikes/create/", views.dislikesCreateView.as_view(), name="modelclasses_dislikes_create"),
    path("modelclasses/dislikes/detail/<int:pk>/", views.dislikesDetailView.as_view(), name="modelclasses_dislikes_detail"),
    path("modelclasses/dislikes/update/<int:pk>/", views.dislikesUpdateView.as_view(), name="modelclasses_dislikes_update"),
    path("modelclasses/dislikes/delete/<int:pk>/", views.dislikesDeleteView.as_view(), name="modelclasses_dislikes_delete"),
    path("modelclasses/expansion/", views.expansionListView.as_view(), name="modelclasses_expansion_list"),
    path("modelclasses/expansion/create/", views.expansionCreateView.as_view(), name="modelclasses_expansion_create"),
    path("modelclasses/expansion/detail/<int:pk>/", views.expansionDetailView.as_view(), name="modelclasses_expansion_detail"),
    path("modelclasses/expansion/update/<int:pk>/", views.expansionUpdateView.as_view(), name="modelclasses_expansion_update"),
    path("modelclasses/expansion/delete/<int:pk>/", views.expansionDeleteView.as_view(), name="modelclasses_expansion_delete"),
    path("modelclasses/game/", views.gameListView.as_view(), name="modelclasses_game_list"),
    path("modelclasses/game/create/", views.gameCreateView.as_view(), name="modelclasses_game_create"),
    path("modelclasses/game/detail/<int:pk>/", views.gameDetailView.as_view(), name="modelclasses_game_detail"),
    path("modelclasses/game/update/<int:pk>/", views.gameUpdateView.as_view(), name="modelclasses_game_update"),
    path("modelclasses/game/delete/<int:pk>/", views.gameDeleteView.as_view(), name="modelclasses_game_delete"),
    path("modelclasses/genre/", views.genreListView.as_view(), name="modelclasses_genre_list"),
    path("modelclasses/genre/create/", views.genreCreateView.as_view(), name="modelclasses_genre_create"),
    path("modelclasses/genre/detail/<int:pk>/", views.genreDetailView.as_view(), name="modelclasses_genre_detail"),
    path("modelclasses/genre/update/<int:pk>/", views.genreUpdateView.as_view(), name="modelclasses_genre_update"),
    path("modelclasses/genre/delete/<int:pk>/", views.genreDeleteView.as_view(), name="modelclasses_genre_delete"),
    path("modelclasses/location/", views.locationListView.as_view(), name="modelclasses_location_list"),
    path("modelclasses/location/create/", views.locationCreateView.as_view(), name="modelclasses_location_create"),
    path("modelclasses/location/detail/<int:pk>/", views.locationDetailView.as_view(), name="modelclasses_location_detail"),
    path("modelclasses/location/update/<int:pk>/", views.locationUpdateView.as_view(), name="modelclasses_location_update"),
    path("modelclasses/location/delete/<int:pk>/", views.locationDeleteView.as_view(), name="modelclasses_location_delete"),

    path("modelclasses/htmx/dislikes/", htmx.HTMXdislikesListView.as_view(), name="modelclasses_dislikes_htmx_list"),
    path("modelclasses/htmx/dislikes/create/", htmx.HTMXdislikesCreateView.as_view(), name="modelclasses_dislikes_htmx_create"),
    path("modelclasses/htmx/dislikes/delete/<int:pk>/", htmx.HTMXdislikesDeleteView.as_view(), name="modelclasses_dislikes_htmx_delete"),
    path("modelclasses/htmx/expansion/", htmx.HTMXexpansionListView.as_view(), name="modelclasses_expansion_htmx_list"),
    path("modelclasses/htmx/expansion/create/", htmx.HTMXexpansionCreateView.as_view(), name="modelclasses_expansion_htmx_create"),
    path("modelclasses/htmx/expansion/delete/<int:pk>/", htmx.HTMXexpansionDeleteView.as_view(), name="modelclasses_expansion_htmx_delete"),
    path("modelclasses/htmx/game/", htmx.HTMXgameListView.as_view(), name="modelclasses_game_htmx_list"),
    path("modelclasses/htmx/game/create/", htmx.HTMXgameCreateView.as_view(), name="modelclasses_game_htmx_create"),
    path("modelclasses/htmx/game/delete/<int:pk>/", htmx.HTMXgameDeleteView.as_view(), name="modelclasses_game_htmx_delete"),
    path("modelclasses/htmx/genre/", htmx.HTMXgenreListView.as_view(), name="modelclasses_genre_htmx_list"),
    path("modelclasses/htmx/genre/create/", htmx.HTMXgenreCreateView.as_view(), name="modelclasses_genre_htmx_create"),
    path("modelclasses/htmx/genre/delete/<int:pk>/", htmx.HTMXgenreDeleteView.as_view(), name="modelclasses_genre_htmx_delete"),
    path("modelclasses/htmx/location/", htmx.HTMXlocationListView.as_view(), name="modelclasses_location_htmx_list"),
    path("modelclasses/htmx/location/create/", htmx.HTMXlocationCreateView.as_view(), name="modelclasses_location_htmx_create"),
    path("modelclasses/htmx/location/delete/<int:pk>/", htmx.HTMXlocationDeleteView.as_view(), name="modelclasses_location_htmx_delete"),
)
