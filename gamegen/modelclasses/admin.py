from django.contrib import admin
from django import forms

from . import models


class dislikesAdminForm(forms.ModelForm):

    class Meta:
        model = models.dislikes
        fields = "__all__"


class dislikesAdmin(admin.ModelAdmin):
    form = dislikesAdminForm
    list_display = [
        "game",
        "location",
        "disliker",
    ]
    search_fields = ('game__name','location__name',)
    list_filter = ('location',)


class expansionAdminForm(forms.ModelForm):

    class Meta:
        model = models.expansion
        fields = "__all__"


class expansionAdmin(admin.ModelAdmin):
    form = expansionAdminForm
    list_display = [
        "name",
        "base_game",
        "number",
        "min_player",
        "max_player",
        "release_date",
        "rule_link",
        "file",
    ]
    search_fields = ('name','base_game__name',)
    list_filter = ('base_game', 'genre', 'teaming',)


class gameAdminForm(forms.ModelForm):

    class Meta:
        model = models.game
        fields = "__all__"


class gameAdmin(admin.ModelAdmin):
    form = gameAdminForm
    list_display = [
        "name",
        "duration",
        "min_player",
        "max_player",
        "release_date",
        "rule_link",
        "file",
    ]
    search_fields = ('name',)
    list_filter = ('genre', 'teaming',)



class genreAdminForm(forms.ModelForm):

    class Meta:
        model = models.genre
        fields = "__all__"


class genreAdmin(admin.ModelAdmin):
    form = genreAdminForm
    list_display = [
        "name",
    ]


class locationAdminForm(forms.ModelForm):

    class Meta:
        model = models.location
        fields = "__all__"


class locationAdmin(admin.ModelAdmin):
    form = locationAdminForm
    list_display = [
        "name",
    ]



admin.site.register(models.dislikes, dislikesAdmin)
admin.site.register(models.expansion, expansionAdmin)
admin.site.register(models.game, gameAdmin)
admin.site.register(models.genre, genreAdmin)
admin.site.register(models.location, locationAdmin)
admin.site.register(models.teaming)