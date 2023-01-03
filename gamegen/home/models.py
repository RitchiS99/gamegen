from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
from django import forms


class TEAMING(models.TextChoices):
    TEAM = 'T', _("Team")
    COOP = 'C', _("Cooperative")
    COMPETITIVE = 'V', _("Competitive")

class GENRE(models.IntegerChoices):
	WORD = '1', _("Word")
	ADVENTURE = '2', _("Adventure")
	REACTION = '3', _("Reaction")
	DICE = '4', _("Dice")
	ROLEPLAY = '5', _("Roleplay")
	THINK = '6', _("Think")
	STRATEGY = '7', _("Strategy")
	CARD = '8', _("Card")
	

class TIME(models.IntegerChoices):
	SHORT = '60', _("Short")
	MIDDLE = '120', _("Middle")
	LONG = '1000000', _("Long")


# Create your models here.
class Ort(models.Model):
	orte_name = models.CharField(max_length = 200, verbose_name=_('modelName'))
	def __str__(self):
		return self.orte_name
	class Meta:
		verbose_name=_('locationModel')
		verbose_name_plural = _('locationModelPlural')
class Genre(models.Model):
	genre_name = models.CharField(max_length = 200, verbose_name=_('modelName'))
	def __str__(self):
		return self.genre_name
	class Meta:
		verbose_name=_('genreModel')
		verbose_name_plural = _('genreModelPlural')
class VS(models.Model):
	versus_name = models.CharField(max_length = 200, verbose_name=_('modelName'))
	def __str__(self):
		return self.versus_name
	class Meta:
		verbose_name=_('versusModel')
		verbose_name_plural = _('versusModelPlural')
class Zeit(models.Model):
	zeit_einteilung = models.CharField(max_length = 200, verbose_name=_('modelName'))
	maxZeit = models.IntegerField(default=0, verbose_name=_('modelMinTime'))
	minZeit = models.IntegerField(default=0, verbose_name=_('modelMaxTime'))
	def __str__(self):
		return self.zeit_einteilung
	class Meta:
		verbose_name=_('timeModel')
		verbose_name_plural = _('timeModelPlural')
class Personen(models.Model):
	name = models.CharField(max_length=200, verbose_name=_('modelName'))
	ort = models.ManyToManyField(Ort, verbose_name=_('locationModel'))
	def __str__(self):
		return self.name
	class Meta:
		verbose_name=_('personModel')
		verbose_name_plural = _('personModelPlural')
class Spiel(models.Model):
	name = models.CharField(max_length=200, verbose_name=_('modelName'))
	teaming = models.CharField(max_length=1, choices=TEAMING.choices, verbose_name=_('versusModel'), default=TEAMING.TEAM)
	group = models.IntegerField(choices=GENRE.choices, default=GENRE.WORD, verbose_name=_("genreModel"))
	ort = models.ForeignKey(Ort, on_delete=CASCADE, verbose_name=_('locationModel'))
	time = models.IntegerField(choices=TIME.choices, default=TIME.SHORT, verbose_name=_("timeModel"))
	minSpieler = models.IntegerField(default=0, verbose_name=_('modelMinPlayer'))
	maxSpieler = models.IntegerField(default=0, verbose_name=_('modelMaxPlayer'))
	dislikes = models.ManyToManyField(Personen, blank=True, verbose_name=_('modelDislikes'))
	rules = models.CharField(default="", blank=True, max_length=8000, verbose_name=_('modelRules'))
	def __str__(self):
		return self.name+' ('+ self.ort.orte_name +')'
	class Meta:
		verbose_name=_('gameModel')
		verbose_name_plural = _('gameModelPlural')
class Erweiterungen(models.Model):
	name = models.CharField(max_length=200, verbose_name=_('modelName'))
	grundspiel = models.ForeignKey(Spiel, on_delete=CASCADE, verbose_name=_('modelBaseGame'))
	minSpieler = models.IntegerField(default=0, verbose_name=_('modelMinPlayer'))
	maxSpieler = models.IntegerField(default=0, verbose_name=_('modelMaxPlayer'))
	nummer = models.IntegerField(default=0, verbose_name=_('modelNumber'))
	def __str__(self):
		return str(self.nummer) + '. ' + self.name + ' (' + self.grundspiel.name+'- ' + self.grundspiel.ort.orte_name + ')'
	class Meta:
		verbose_name=_('extensionModel')
		verbose_name_plural = _('extensionModelPlural')
class Rechte(models.Model):
	person = models.OneToOneField(User, on_delete=CASCADE, verbose_name=_('personModel'))
	viewer = models.ManyToManyField(Ort, related_name="viewer", blank=True, verbose_name=_('modelViewer'))
	editer = models.ManyToManyField(Ort, related_name="editer", blank=True, verbose_name=_('modelEditer'))
	creater = models.ManyToManyField(Ort, related_name="creater", blank=True, verbose_name=_('modelCreater'))
	def __str__(self):
		return self.person.username
	class Meta:
		verbose_name=_('permissionModel')
		verbose_name_plural = _('permissionModelPlural')

# Group.add_to_class('Ort', models.ManyToManyField(Ort,blank=True))

Permissions = (
	    ('C', 'Creator'),
        ('E', 'Editor'),
        ('V', 'Viewer'),
    )

# Group.add_to_class('Permission', models.CharField(max_length=1, choices=Permissions))
