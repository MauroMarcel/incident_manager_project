from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from incidents.models import Incidente
from .models import Reporte


class ReporteHomeView(LoginRequiredMixin, TemplateView):
    """Página principal de reportes con resumen general"""
    template_name = 'reports/reporte_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Totales generales
        context['total_incidentes'] = Incidente.objects.count()
        context['total_abiertos'] = Incidente.objects.exclude(
            estado__in=['CER', 'RES', 'RCH']
        ).count()
        context['total_cerrados'] = Incidente.objects.filter(
            estado__in=['CER', 'RES']
        ).count()
        context['total_rechazados'] = Incidente.objects.filter(
            estado='RCH'
        ).count()

        # Por estado
        context['por_estado'] = Incidente.objects.values(
            'estado'
        ).annotate(total=Count('id')).order_by('estado')

        # Por impacto
        context['por_impacto'] = Incidente.objects.values(
            'impacto'
        ).annotate(total=Count('id')).order_by('impacto')

        # Por tipo
        context['por_tipo'] = Incidente.objects.values(
            'tipo_incidente__name'
        ).annotate(total=Count('id')).order_by('-total')

        # Últimos 5 incidentes
        context['ultimos_incidentes'] = Incidente.objects.select_related(
            'tipo_incidente', 'reportado_por'
        ).order_by('-fecha_reporte')[:5]

        return context


class IncidenteFichaView(LoginRequiredMixin, DetailView):
    """Ficha individual de un incidente lista para imprimir"""
    model = Incidente
    template_name = 'reports/incidente_ficha.html'
    context_object_name = 'incidente'