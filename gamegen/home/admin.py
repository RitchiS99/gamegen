from django.contrib import admin
from .models import Ort, Genre, Personen, Zeit, VS, Spiel, Erweiterungen, Rechte
# Register your models here.
admin.site.register(Ort)
admin.site.register(Genre)
admin.site.register(Zeit)
admin.site.register(VS)

class SpielAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre','vs','ort','zeit',)
    search_fields = ('name',)
    list_filter = ('genre', 'vs', 'ort', 'zeit',)
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

