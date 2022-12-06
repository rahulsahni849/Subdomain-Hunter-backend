from rest_framework import serializers
from subdomain_app.models import SubdomainDetails

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubdomainDetails
        fields = '__all__'
