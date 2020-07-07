from django.urls import path

from .views import CombatListView, Income

app_name='combat'

urlpatterns = [
    path('list/', CombatListView.as_view(), name='combat_list'),
    path('add/<pk>', Income.as_view(), name='add'),
]