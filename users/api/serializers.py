from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db.models.query_utils import Q

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):

        password = self.validated_data['password']
        password1= self.validated_data['password2']

        if password != password1:
            raise serializers.ValidationError({'error':"password doesn't matched"})
        
        v=self.validated_data

        if User.objects.filter(Q(email=v['email']) | Q(username=v['username'])).exists():
            raise serializers.ValidationError({'error':'Account already exists'})
        
        user = User(email=v['email'],username=v['username'])
        user.set_password(password)
        user.save()

        return user