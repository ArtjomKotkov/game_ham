from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-api/', include('rest_framework.urls')),
    path('api/v1/', include('hero_app.urls')),
    path('auth/', include('main_app.urls')),
    path('user/', include('user_app.urls')),
    path('combat/', include('combat_app.urls'))
]
