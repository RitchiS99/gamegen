from rest_framework import serializers

from . import models


class dislikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.dislikes
        fields = [
            "disliker",
            "game",
            "location",
        ]

class expansionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.expansion
        fields = [
            "rule_link",
            "release_date",
            "number",
            "name",
            "max_player",
            "min_player",
            "teaming",
            "base_game",
        ]

class gameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.game
        fields = [
            "rule_link",
            "teaming",
            "name",
            "max_player",
            "release_date",
            "duration",
            "min_player",
            "genre",
        ]

class genreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.genre
        fields = [
            "name",
        ]

class locationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.location
        fields = [
            "name",
            "wishlist_games",
            "creater",
            "viewer",
            "expansions",
            "wishlist_expansions",
            "editer",
            "game",
        ]
