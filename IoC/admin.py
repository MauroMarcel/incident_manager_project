from django.contrib import admin
from .models import IoC

class IoCAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_ioc', 'valor')
    search_fields = ('valor',)  

admin.site.register(IoC,IoCAdmin)

