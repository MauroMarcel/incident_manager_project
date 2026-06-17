from django.contrib import admin
from organization.models import Area

class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'area_superior')
    list_display_links = ('nombre',)


admin.site.register(Area,AreaAdmin)