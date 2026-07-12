from django.contrib import admin
from organization.models import Area

class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'area_superior')
    list_display_links = ('nombre',)

    def formfield_for_foreignkey(self, db_field, request, obj=None, **kwargs):
        if db_field.name == 'area_superior' and obj:
            exclude_ids = self._get_descendant_ids(obj)
            kwargs['queryset'] = Area.objects.exclude(pk__in=exclude_ids)
        return super().formfield_for_foreignkey(db_field, request, obj=obj, **kwargs)

    def _get_descendant_ids(self, area):
        ids = [area.pk]
        for sub in area.subareas.all():
            ids.extend(self._get_descendant_ids(sub))
        return ids


admin.site.register(Area, AreaAdmin)