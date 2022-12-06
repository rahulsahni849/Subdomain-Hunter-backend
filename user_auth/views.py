from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user_auth.serializers import UserRegisterSerializer,UserLoginSerializer,UserProfileSerializer,CustomJWTTokenSerializer
from django.contrib.auth import authenticate
from user_auth.renderers import CustomRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
class UserRegisterationViews(APIView):
    renderer_classes=[CustomRenderer]
    def post(self,request,format=None):
        serializer = UserRegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"msg":f"Registrations successful for {user.email}","token":token,"status":status.HTTP_201_CREATED})
        return Response(serializer.errors)

class UserLoginViews(APIView):
    renderer_classes=[CustomRenderer]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if(user is not None):
                token = get_tokens_for_user(user)
                return Response({"msg":f"login successful for {user.email}","token":token,"status":status.HTTP_200_OK})
            else:
                return Response({"error":f"login failed","status":status.HTTP_401_UNAUTHORIZED})
        return Response({"error":serializer.errors,'status':status.HTTP_400_BAD_REQUEST}
        )

class UserProfileViews(APIView):
    renderer_classes=[CustomRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        print(request)
        try:
            serializer = UserProfileSerializer(request.user)
            return Response({'user':serializer.data,'status':status.HTTP_200_OK})
        except Exception:
            return Response({'error':'internal server error','status':status.HTTP_400_BAD_REQUEST})


def get_tokens_for_user(user):
    refresh = CustomJWTTokenSerializer.get_token(user)
    # print(refresh)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }