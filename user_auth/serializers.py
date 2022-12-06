from rest_framework import serializers
from user_auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields=['email','name','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self,attr):
        #print(attr)
        password=attr.get('password')
        password2=attr.get('password2')
        if password!=password2:
            raise serializers.ValidationError("password doesn't match!")
        return attr

    def create(self,valid_data):
        return User.objects.create_user(**valid_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        model = User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','name','email']

class CustomJWTTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.name
        return token
