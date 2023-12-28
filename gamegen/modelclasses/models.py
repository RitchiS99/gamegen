from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField



class teaming(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return str(self.name)

class dislikes(models.Model):

    # Relationships
    game = models.ForeignKey("modelclasses.game", on_delete=models.CASCADE)
    location = models.ForeignKey("modelclasses.location", on_delete=models.CASCADE)

    # Fields
    disliker = models.TextField(max_length=200,null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.game.name + " - " + self.location.name)

    def get_absolute_url(self):
        return reverse("modelclasses_dislikes_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("modelclasses_dislikes_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("modelclasses_dislikes_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("modelclasses_dislikes_htmx_delete", args=(self.pk,))


class expansion(models.Model):
    name = models.CharField(max_length=60)
    # Relationships
    base_game = models.ForeignKey("modelclasses.game", on_delete=models.CASCADE)
    number = models.IntegerField()
    genre = models.ManyToManyField("modelclasses.genre", blank=True)
    teaming = models.ManyToManyField("modelclasses.teaming", blank=True)
    duration = models.IntegerField()
    min_player = models.IntegerField()
    max_player = models.IntegerField()
    # Fields
    release_date = models.DateField(null=True, blank=True)
    rule_link = models.URLField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name+" - "+self.base_game.name)

    def get_absolute_url(self):
        return reverse("modelclasses_expansion_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("modelclasses_expansion_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("modelclasses_expansion_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("modelclasses_expansion_htmx_delete", args=(self.pk,))


class game(models.Model):
    name = models.CharField(max_length=50)
    # Relationships
    genre = models.ManyToManyField("modelclasses.genre", blank=True)
    teaming = models.ManyToManyField("modelclasses.teaming", blank=True)
    duration = models.IntegerField()
    # Fields
    min_player = models.IntegerField()
    max_player = models.IntegerField()
    release_date = models.DateField(null=True, blank=True)
    rule_link = models.URLField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("modelclasses_game_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("modelclasses_game_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("modelclasses_game_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("modelclasses_game_htmx_delete", args=(self.pk,))


class genre(models.Model):

    # Fields
    name = models.CharField(max_length=60)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("modelclasses_genre_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("modelclasses_genre_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("modelclasses_genre_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("modelclasses_genre_htmx_delete", args=(self.pk,))


class location(models.Model):
    name = models.CharField(max_length=60)
    creater = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="creater")
    editer = models.ManyToManyField("auth.User", related_name="editer", blank=True)
    viewer = models.ManyToManyField("auth.User", related_name="viewer", blank=True)
    # Relationships
    game = models.ManyToManyField("modelclasses.game", through='dislikes', blank=True)
    expansions = models.ManyToManyField("modelclasses.expansion", related_name="expansions", blank=True)

    wishlist_games = models.ManyToManyField("modelclasses.game", related_name="wishlist_games", blank=True)
    wishlist_expansions = models.ManyToManyField("modelclasses.expansion", related_name="wishlist_expansions", blank=True)
    
    disliker = models.TextField(max_length=200,null=True, blank=True)
    

    # Fields


    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("modelclasses_location_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("modelclasses_location_update", args=(self.pk,))

    @staticmethod
    def get_htmx_create_url():
        return reverse("modelclasses_location_htmx_create")

    def get_htmx_delete_url(self):
        return reverse("modelclasses_location_htmx_delete", args=(self.pk,))
