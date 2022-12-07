from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .renderers import CustomRenderer
from rest_framework.permissions import IsAuthenticated
import time
from .models import DomainSearchHistory,SubdomainDetails
from .serializers import DomainSerializer,JsonSerializer
from django.core.exceptions import ObjectDoesNotExist
import json
from rest_framework import serializers

# from .services import sublist3r
from .services.domain_enumerator_service import  domain_enumerator

from django.core.serializers import serialize

class DomainEnumeratorView(APIView):
    renderer_classes=[CustomRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        domain_name = request.data.get('name').strip()
        # print(domain_name)
        response=None
        serializer = JsonSerializer()
        try:
            domain=DomainSearchHistory.objects.get(domain_name=domain_name)
            subdomains=SubdomainDetails.objects.filter(domain_name=domain)
            
            response= serializer.serialize(subdomains)
            print(response)
            return Response({"result":json.loads(response),'status':status.HTTP_200_OK})
        except ObjectDoesNotExist:
            data = self.domain_data_save(domain_name)
            if(data=="error"):
                return Response({"error":"enumerator service error",'status':status.HTTP_200_OK})
            response= serializer.serialize(data)
            print(response)
            return Response({"result":json.loads(response),'status':status.HTTP_200_OK})
        # except Exception:
        #     return Response({"data":Exception,'status':status.HTTP_500_INTERNAL_SERVER_ERROR})

            
        
            
    
    def domain_data_save(self,domain_name):
        try:
            print("service started...")
            start_time=time.perf_counter()
            data = domain_enumerator(domain_name)
            if(len(data)==0):
                return []
            # print(data)
            end_time=time.perf_counter()
            dict_of_objs=dict()
            domain=DomainSearchHistory.objects.create(domain_name=domain_name)

            # adding subdomains and ports
            for key,value in data[0].get("ports").items():
                sub_domain=SubdomainDetails(subdomain_name=key,ports=",".join([str(x) for x in value]),domain_name=domain)
                dict_of_objs[key]=sub_domain

            # adding subdomains details
            for i in data[1].get("details"):
                temp_obj = dict_of_objs[i['subdomain_name']]
                temp_obj.cname=i['cname']
                temp_obj.webserver=i['web_server']
                temp_obj.ip=i['ip']
                temp_obj.page_title=i['page_title']
                temp_obj.status_code=i['status_code']
                temp_obj.content_length=i['content_length']
                temp_obj.content_type=i['content_type']
                temp_obj.tech_stack_detect=i['tech_stack_detect']
                temp_obj.response_time=i['response_time']
                # temp_obj.ipv6=i['ipv6']
            # adding subdomains screenshots
            for i in data[2].get("images"):
                temp_obj = dict_of_objs[i['subdomain_name']]
                temp_obj.screenshot_path = i['screenshot_path']
                temp_obj.save()
            domain.save()
            
            print(f"Program finished in {round(end_time-start_time,4)} seconds")
            print("service ended...")
            # print(dict_of_objs.values())
            return dict_of_objs.values()
        except Exception:
            return "Error"
        # print(dict_of_objs)

