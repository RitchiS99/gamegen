from django.contrib import admin
from .models import Ort, Genre, Personen, Zeit, VS, Spiel, Erweiterungen, Rechte
# from modeltranslation.admin import TranslationAdmin

# class GenreAdmin(TranslationAdmin):
#     pass
# class VersusAdmin(TranslationAdmin):
#     pass
# class ZeitAdmin(TranslationAdmin):
#     pass

# admin.site.register(Genre, GenreAdmin)
# admin.site.register(VS, VersusAdmin)
# admin.site.register(Zeit, ZeitAdmin)


# Register your models here.
admin.site.register(Ort)
admin.site.register(Genre)
admin.site.register(Zeit)
admin.site.register(VS)

class SpielAdmin(admin.ModelAdmin):
    list_display = ('name', 'group','teaming','ort','time',)
    search_fields = ('name',)
    list_filter = ('group', 'teaming', 'ort', 'time',)
    pass
class ErweiterungAdmin(admin.ModelAdmin):
    search_fields = ('grundspiel__name', 'name',)
    list_display = ('name', 'grundspiel')
    pass

class PersonenAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('ort',)
    pass
class RechteAdmin(admin.ModelAdmin):
    search_fields = ('person__username',)

admin.site.register(Spiel, SpielAdmin)
admin.site.register(Erweiterungen, ErweiterungAdmin)
admin.site.register(Personen, PersonenAdmin)
admin.site.register(Rechte, RechteAdmin)

