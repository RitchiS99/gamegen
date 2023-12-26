from rest_framework import viewsets, permissions

from . import serializers
from . import models


class dislikesViewSet(viewsets.ModelViewSet):
    """ViewSet for the dislikes class"""

    queryset = models.dislikes.objects.all()
    serializer_class = serializers.dislikesSerializer
    permission_classes = [permissions.IsAuthenticated]


class expansionViewSet(viewsets.ModelViewSet):
    """ViewSet for the expansion class"""

    queryset = models.expansion.objects.all()
    serializer_class = serializers.expansionSerializer
    permission_classes = [permissions.IsAuthenticated]


class gameViewSet(viewsets.ModelViewSet):
    """ViewSet for the game class"""

    queryset = models.game.objects.all()
    serializer_class = serializers.gameSerializer
    permission_classes = [permissions.IsAuthenticated]


class genreViewSet(viewsets.ModelViewSet):
    """ViewSet for the genre class"""

    queryset = models.genre.objects.all()
    serializer_class = serializers.genreSerializer
    permission_classes = [permissions.IsAuthenticated]


class locationViewSet(viewsets.ModelViewSet):
    """ViewSet for the location class"""

    queryset = models.location.objects.all()
    serializer_class = serializers.locationSerializer
    permission_classes = [permissions.IsAuthenticated]
