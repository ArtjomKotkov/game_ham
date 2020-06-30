from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .serializers import HeroShortSerializer, HeroFullSerializer
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
    def get(self, request):
        data = request.GET
        mode = data.get('short', 'false')
        ids = data.get('ids', None)
        if ids:
            heroes = Hero.objects.filter(id__in=query_list_to_list_of_int(ids, ','))
        else:
            heroes = Hero.objects.all()
        if mode == 'false':
            serializer = HeroFullSerializer(heroes, many=True)
        else:
            serializer = HeroShortSerializer(heroes, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        Create hero for user with id = user_id.
        Params:
            -hero_class: archer, knight, wizard
        """
        data = request.POST
        hero_class = data.get('hero_class', None)
        user = data.get('user_id', None)
        if not user:
            return Response(dict(status='Request error'), status=400)



