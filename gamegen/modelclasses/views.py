from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms


class dislikesListView(generic.ListView):
    model = models.dislikes
    form_class = forms.dislikesForm


class dislikesCreateView(generic.CreateView):
    model = models.dislikes
    form_class = forms.dislikesForm


class dislikesDetailView(generic.DetailView):
    model = models.dislikes
    form_class = forms.dislikesForm


class dislikesUpdateView(generic.UpdateView):
    model = models.dislikes
    form_class = forms.dislikesForm
    pk_url_kwarg = "pk"


class dislikesDeleteView(generic.DeleteView):
    model = models.dislikes
    success_url = reverse_lazy("modelclasses_dislikes_list")


class expansionListView(generic.ListView):
    model = models.expansion
    form_class = forms.expansionForm


class expansionCreateView(generic.CreateView):
    model = models.expansion
    form_class = forms.expansionForm


class expansionDetailView(generic.DetailView):
    model = models.expansion
    form_class = forms.expansionForm


class expansionUpdateView(generic.UpdateView):
    model = models.expansion
    form_class = forms.expansionForm
    pk_url_kwarg = "pk"


class expansionDeleteView(generic.DeleteView):
    model = models.expansion
    success_url = reverse_lazy("modelclasses_expansion_list")


class gameListView(generic.ListView):
    model = models.game
    form_class = forms.gameForm


class gameCreateView(generic.CreateView):
    model = models.game
    form_class = forms.gameForm


class gameDetailView(generic.DetailView):
    model = models.game
    form_class = forms.gameForm


class gameUpdateView(generic.UpdateView):
    model = models.game
    form_class = forms.gameForm
    pk_url_kwarg = "pk"


class gameDeleteView(generic.DeleteView):
    model = models.game
    success_url = reverse_lazy("modelclasses_game_list")


class genreListView(generic.ListView):
    model = models.genre
    form_class = forms.genreForm


class genreCreateView(generic.CreateView):
    model = models.genre
    form_class = forms.genreForm


class genreDetailView(generic.DetailView):
    model = models.genre
    form_class = forms.genreForm


class genreUpdateView(generic.UpdateView):
    model = models.genre
    form_class = forms.genreForm
    pk_url_kwarg = "pk"


class genreDeleteView(generic.DeleteView):
    model = models.genre
    success_url = reverse_lazy("modelclasses_genre_list")


class locationListView(generic.ListView):
    model = models.location
    form_class = forms.locationForm


class locationCreateView(generic.CreateView):
    model = models.location
    form_class = forms.locationForm


class locationDetailView(generic.DetailView):
    model = models.location
    form_class = forms.locationForm


class locationUpdateView(generic.UpdateView):
    model = models.location
    form_class = forms.locationForm
    pk_url_kwarg = "pk"


class locationDeleteView(generic.DeleteView):
    model = models.location
    success_url = reverse_lazy("modelclasses_location_list")
