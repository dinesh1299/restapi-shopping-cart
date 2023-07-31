from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('first_app.api.urls')),
    path('auth/',include('users.api.urls')),
    path('api-path/',include('rest_framework.urls'))
]
