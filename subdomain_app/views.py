from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .renderers import CustomRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .services import sublist3r
import threading
import time

# from .services import sublist3r
from .services.domain_enumerator_service import  domain_enumerator

class DomainEnumeratorView(APIView):
    renderer_classes=[CustomRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        # print(request.user)
        domain_name = request.data.get('name')
        print("services started...")
        start_time=time.perf_counter()
        data = domain_enumerator(domain_name)
        print(data)
        end_time=time.perf_counter()
        print(f"Program finished in {round(end_time-start_time,4)} seconds")
        print("services ended...")
        try:
            serializer = UserProfileSerializer(request.user)
            return Response({'user':serializer.data,'status':status.HTTP_200_OK})
        except Exception:
            return Response({'error':'internal server error','status':status.HTTP_400_BAD_REQUEST})
