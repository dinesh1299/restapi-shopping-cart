from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('login',obtain_auth_token, name='login'),
    path('register', views.RegisterUser.as_view(),name="register_user"),  
    path('logout', views.LogoutUser.as_view(),name="logout_user"),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      
]