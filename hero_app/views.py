from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import HeroShortSerializer, HeroFullSerializer, SpellShortSerializer, SpellFullSerializer
from .models import Hero, Spell
from .services import Heroes


# All api views provides short and full mode, that can be set in GET params as short=true/false.

def query_list_to_list_of_int(string: str, delimiter: str):
    result = []
    for elem in string.split(delimiter):
        try:
            result.append(int(elem))
        except:
            pass
    return result

def check_exist(model, pk):
    try:
        instance = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return instance

def make_serializer(mode, short_serializer, full_serializer, model, many:bool):
    print(mode)
    if mode == 'false':
        serializer = full_serializer(model, many=many)
    else:
        serializer = short_serializer(model, many=many)
    return serializer

class CustomAPIView(APIView):
    short_serializer = None
    full_serializer = None
    model = None

    def get(self, request, pk=None):
        data = request.GET
        mode = data.get('short', 'false')
        ids = data.get('ids', None)
        user_id = data.get('user_id', None)
        if pk:
            instance = check_exist(self.model, pk)
            serializer = make_serializer(mode, self.short_serializer, self.full_serializer, instance, False)
            return Response(serializer.data, status=200)
        try:
            user = User.objects.get(pk=int(user_id))
            instances = self.model.objects.filter(user=user)
        except (TypeError, ValueError):
            if ids:
                instances = self.model.objects.filter(id__in=query_list_to_list_of_int(ids, ','))
            else:
                instances = self.model.objects.all()
        except self.model.DoesNotExist:
            instances = None
        serializer = make_serializer(mode, self.short_serializer, self.full_serializer, instances, True)
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.model.delete()
        return Response(status=status.HTTP_200_OK)


class HeroApi(APIView):
    """
    Hero API.
    Params:
        -ids: list[int] ids which heroes need to return| scheme ids=1,2,3,4,5
    """

    def get(self, request, pk=None):
        data = request.GET
        mode = data.get('short', 'false').lower()
        if pk:
            heroes = check_exist(Hero, pk)
            serializer = make_serializer(mode, HeroShortSerializer, HeroFullSerializer, heroes, False)
            return Response(serializer.data, status=200)
        ids = data.get('ids', None)
        user_id = data.get('user_id', None)
        try:
            user = User.objects.get(pk=int(user_id))
            heroes = Hero.objects.filter(user=user)
        except (TypeError, ValueError):
            if ids:
                heroes = Hero.objects.filter(id__in=query_list_to_list_of_int(ids, ','))
            else:
                heroes = Hero.objects.all()
        except User.DoesNotExist:
            heroes = None
        serializer = make_serializer(mode, HeroShortSerializer, HeroFullSerializer, heroes, True)
        return Response(serializer.data, status=200)

    def post(self, request):

        serializer = HeroFullSerializer(data=request.data)
        if serializer.is_valid():
            hero = serializer.save()
            return Response(HeroFullSerializer(hero, many=False).data, status=201)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            hero_instance = Hero.objects.get(pk=pk)
        except Hero.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HeroFullSerializer(data=request.data, instance=hero_instance)
        if serializer.is_valid():
            hero = serializer.save()
            return Response(HeroFullSerializer(hero, many=False).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            hero_instance = Hero.objects.get(pk=pk)
        except Hero.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        hero_instance.delete()
        return Response(status=status.HTTP_200_OK)


# class Spells(APIView):
#     def get(self, request, pk=None):
#         data = request.GET
#         mode = data.get('short', 'false')
#         if pk:
#             spell = check_exist(Spell, pk)
#             serializer = make_serializer(mode, SpellShortSerializer, SpellFullSerializer, spell, True)

class SpellsApi(CustomAPIView):
    short_serializer = SpellShortSerializer
    full_serializer = SpellFullSerializer
    model = Spell
