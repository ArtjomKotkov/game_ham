from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import HeroShortSerializer, HeroFullSerializer, HeroCreateSerializer
from .models import Hero
from .services import Heroes
# All api views provides short and full mode, that can be set in GET params as short=true/false.

def query_list_to_list_of_int(string:str, delimiter:str):
    result = []
    for elem in string.split(delimiter):
        try:
            result.append(int(elem))
        except:
            pass
    return result

class HeroApi(APIView):
    """
    Hero API.
    Params:
        -ids: list[int] ids which heroes need to return| scheme ids=1,2,3,4,5
    """
    def get(self, request, pk=None):
        data = request.GET
        mode = data.get('short', 'false')
        if pk:
            heroes = Hero.objects.get(pk=pk)
            if mode == 'false':
                serializer = HeroFullSerializer(heroes, many=False)
            else:
                serializer = HeroShortSerializer(heroes, many=False)
            return Response(serializer.data, status=200)
        ids = data.get('ids', None)
        user_id = data.get('user_id', None)
        try:
            user = User.objects.get(pk=int(user_id))
            heroes = Hero.objects.filter(user=user)
        except TypeError:
            if ids:
                heroes = Hero.objects.filter(id__in=query_list_to_list_of_int(ids, ','))
            else:
                heroes = Hero.objects.all()
        except User.DoesNotExist:
            heroes = None
        if mode == 'false':
            serializer = HeroFullSerializer(heroes, many=True)
        else:
            serializer = HeroShortSerializer(heroes, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):

        serializer = HeroCreateSerializer(data=request.data)
        if serializer.is_valid():
            hero = serializer.create(serializer.validated_data)
            return Response(HeroFullSerializer(hero, many=False).data, status=201)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

