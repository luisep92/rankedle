import random
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Map, Difficulty, MapDifficulty, PermittedName, User, Score


# Create your views here.
def IndexView(request):
    return render(request, "index.html")


class MapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map
        fields = [
            'id',
            'duration',
            'name',
            'subname',
            'author',
            'mapper',
            'upload_date',
            'download_url',
            'cover_url',
        ]


class SongViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    @action(detail=False, methods=['get'])
    def random(self, request):
        random_map = random.choice(Map.objects.all())
        serializer = MapSerializer(random_map)
        return Response(serializer.data)
