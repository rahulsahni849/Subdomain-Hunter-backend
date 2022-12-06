from rest_framework import serializers
from user_auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','name','email']
