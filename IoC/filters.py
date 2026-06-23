import django_filters
from .models import IoC

class IoCFilter(django_filters.FilterSet):
    class Meta:
        model = IoC
        fields = {
            'valor': ['icontains'],
            'tipo_ioc': ['exact'],
        }