from rest_framework import serializers
from subdomain_app.models import SubdomainDetails
from django.core.serializers import json

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubdomainDetails
        fields = '__all__'
    
class JsonSerializer(json.Serializer):

    def get_dump_object(self, obj):
        return self._current    