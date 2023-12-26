from django import forms
from modelclasses.models import game
from modelclasses.models import location
from modelclasses.models import game
from modelclasses.models import genre
from modelclasses.models import game
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from modelclasses.models import expansion
from modelclasses.models import expansion
from django.contrib.auth.models import User
from modelclasses.models import game
from . import models


class dislikesForm(forms.ModelForm):
    class Meta:
        model = models.dislikes
        fields = [
            "disliker",
            "game",
            "location",
        ]

    def __init__(self, *args, **kwargs):
        super(dislikesForm, self).__init__(*args, **kwargs)
        self.fields["game"].queryset = game.objects.all()
        self.fields["location"].queryset = location.objects.all()



class expansionForm(forms.ModelForm):
    class Meta:
        model = models.expansion
        fields = [
            "name",
            "base_game",
            "number",
            "teaming",
            "min_player",
            "max_player",
            "release_date",
            "rule_link",
            "file",
        ]

    def __init__(self, *args, **kwargs):
        super(expansionForm, self).__init__(*args, **kwargs)
        self.fields["base_game"].queryset = game.objects.all()



class gameForm(forms.ModelForm):
    class Meta:
        model = models.game
        fields = [
            "name",
            "genre",
            "teaming",
            "duration",
            "min_player",
            "max_player",
            "release_date",
            "rule_link",
            "file",
        ]

    def __init__(self, *args, **kwargs):
        super(gameForm, self).__init__(*args, **kwargs)
        self.fields["genre"].queryset = genre.objects.all()



class genreForm(forms.ModelForm):
    class Meta:
        model = models.genre
        fields = [
            "name",
        ]

class teamingForm(forms.ModelForm):
    class Meta:
        model = models.teaming
        fields = [
            "name",
        ]


class locationForm(forms.ModelForm):
    class Meta:
        model = models.location
        fields = [
            "name",
            "creater",
            "editer",
            "viewer",
            "game",
            "expansions",
            "wishlist_games",
            "wishlist_expansions",
        ]

    def __init__(self, *args, **kwargs):
        super(locationForm, self).__init__(*args, **kwargs)
        self.fields["wishlist_games"].queryset = game.objects.all()
        self.fields["creater"].queryset = User.objects.all()
        self.fields["viewer"].queryset = User.objects.all()
        self.fields["expansions"].queryset = expansion.objects.all()
        self.fields["wishlist_expansions"].queryset = expansion.objects.all()
        self.fields["editer"].queryset = User.objects.all()
        self.fields["game"].queryset = game.objects.all()

