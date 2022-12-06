from django.db import models

class DomainSearchHistory(models.Model):
    domain_name = models.CharField(max_length=255,unique=True)

    def __str__(self) -> str:
        return str(self.domain_name)


class SubdomainDetails(models.Model):
    subdomain_name=models.CharField(max_length=255)
    cname=models.CharField(max_length=255)
    webserver=models.CharField(max_length=255)
    ip=models.CharField(max_length=255)
    page_title=models.CharField(max_length=255)
    status_code=models.CharField(max_length=255)
    response_time=models.CharField(max_length=255)
    tech_stack_detect=models.CharField(max_length=255)
    content_type=models.CharField(max_length=255)
    content_length=models.CharField(max_length=255)
    ipv6=models.CharField(max_length=255)
    ports=models.CharField(max_length=255)
    screenshot_path=models.CharField(max_length=255)
    domain_name = models.ForeignKey(DomainSearchHistory, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.subdomain_name)

    
