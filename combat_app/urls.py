from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import CombatListView, Income, CombatApi, FieldsApi, cobmat


app_name='combat'

urlpatterns = [
    path('list/', CombatListView.as_view(), name='combat_list'),
    path('add/<pk>', Income.as_view(), name='add'),
    path('combat/<pk>', CombatApi.as_view()),
    path('combat/', CombatApi.as_view()),
    path('in_battle/<pk>', cobmat, name='combat_page'),
    path('fields/', FieldsApi.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)