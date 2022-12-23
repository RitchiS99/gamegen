from modeltranslation.translator import translator, TranslationOptions
from .models import *

class GenreTranslationOptions(TranslationOptions):
    fields = ('genre_name',)

class VersusTranslationOptions(TranslationOptions):
    fields = ('versus_name',)

class ZeitTranslationOptions(TranslationOptions):
    fields = ('zeit_einteilung',)

class SpielTranslationOptions(TranslationOptions):
    fields = ('rules',)

translator.register(Genre, GenreTranslationOptions)
translator.register(VS, VersusTranslationOptions)
translator.register(Zeit, ZeitTranslationOptions)
translator.register(Spiel, SpielTranslationOptions)