from django.urls import path
from .views import DomainEnumeratorView

urlpatterns = [
    path('subdomains/', DomainEnumeratorView.as_view(),name="domain-enumerate"),
]
