import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

from modelclasses import models as modelclasses_models
from home import models as home_models


def random_string(length=10):
    # Create a random string of length length
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def create_User(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_AbstractUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractUser.objects.create(**defaults)


def create_AbstractBaseUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractBaseUser.objects.create(**defaults)


def create_Group(**kwargs):
    defaults = {
        "name": "%s_group" % random_string(5),
    }
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_ContentType(**kwargs):
    defaults = {
    }
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_modelclasses_dislikes(**kwargs):
    defaults = {}
    defaults["disliker"] = ""
    if "game" not in kwargs:
        defaults["game"] = create_modelclasses_game()
    if "location" not in kwargs:
        defaults["location"] = create_modelclasses_location()
    defaults.update(**kwargs)
    return modelclasses_models.dislikes.objects.create(**defaults)
def create_modelclasses_expansion(**kwargs):
    defaults = {}
    defaults["rule_link"] = ""
    defaults["release_date"] = datetime.now()
    defaults["number"] = ""
    defaults["name"] = ""
    defaults["max_player"] = ""
    defaults["min_player"] = ""
    defaults["teaming"] = ""
    if "base_game" not in kwargs:
        defaults["base_game"] = create_modelclasses_game()
    defaults.update(**kwargs)
    return modelclasses_models.expansion.objects.create(**defaults)
def create_modelclasses_game(**kwargs):
    defaults = {}
    defaults["rule_link"] = ""
    defaults["teaming"] = ""
    defaults["name"] = ""
    defaults["max_player"] = ""
    defaults["release_date"] = datetime.now()
    defaults["duration"] = ""
    defaults["min_player"] = ""
    if "genre" not in kwargs:
        defaults["genre"] = create_modelclasses_genre()
    defaults.update(**kwargs)
    return modelclasses_models.game.objects.create(**defaults)
def create_modelclasses_genre(**kwargs):
    defaults = {}
    defaults["name"] = ""
    defaults.update(**kwargs)
    return modelclasses_models.genre.objects.create(**defaults)
def create_modelclasses_location(**kwargs):
    defaults = {}
    defaults["name"] = ""
    if "wishlist_games" not in kwargs:
        defaults["wishlist_games"] = create_modelclasses_game()
    if "creater" not in kwargs:
        defaults["creater"] = create_User()
    if "viewer" not in kwargs:
        defaults["viewer"] = create_User()
    if "expansions" not in kwargs:
        defaults["expansions"] = create_modelclasses_expansion()
    if "wishlist_expansions" not in kwargs:
        defaults["wishlist_expansions"] = create_modelclasses_expansion()
    if "editer" not in kwargs:
        defaults["editer"] = create_User()
    if "game" not in kwargs:
        defaults["game"] = create_modelclasses_game()
    defaults.update(**kwargs)
    return modelclasses_models.location.objects.create(**defaults)
