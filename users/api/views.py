from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class LogoutUser(APIView):
    def post(self,request):
        request.user.auth_token.delete()
        return Response('Logout sucessfully')


class RegisterUser(APIView):
    def post(self,request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['username'] = user.username
            data['email'] = user.email
            token = Token.objects.get(user = user).key
            data['token'] = token
        else:
            data = serializer.errors
        
        return Response(data)
    