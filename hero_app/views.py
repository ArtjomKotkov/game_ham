from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import HeroShortSerializer, HeroFullSerializer,\
    SpellShortSerializer, SpellFullSerializer, \
    SpellTomeFullSerializer, SpellTomeShortSerializer
from .models import Hero, Spell, SpellTome


# All api views provides short and full mode, that can be set in GET params as short=true/false.

def query_list_to_list_of_int(string: str, delimiter: str):
    result = []
    for elem in string.split(delimiter):
        try:
            result.append(int(elem))
        except:
            pass
    return result


def make_serializer(mode, short_serializer, full_serializer, model, many: bool):
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
            try:
                instance = self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
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

    def post(self, request):
        data = request.GET
        mode = data.get('short', 'false')
        serializer = self.full_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_output = make_serializer(mode, self.short_serializer, self.full_serializer, instance, False)
            return Response(serializer_output.data, status=201)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        data = request.GET
        mode = data.get('short', 'false')
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.full_serializer(data=request.data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save()
            serializer_output = make_serializer(mode, self.short_serializer, self.full_serializer, instance, False)
            return Response(serializer_output.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            instance = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_200_OK)


class HeroApi(CustomAPIView):
    short_serializer = HeroShortSerializer
    full_serializer = HeroFullSerializer
    model = Hero

class SpellsApi(CustomAPIView):
    short_serializer = SpellShortSerializer
    full_serializer = SpellFullSerializer
    model = Spell

class SpelTomesApi(CustomAPIView):
    short_serializer = SpellTomeShortSerializer
    full_serializer = SpellTomeFullSerializer
    model = SpellTome