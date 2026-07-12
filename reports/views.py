from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.urls import reverse_lazy
from django.db.models import Count, Max
from incidents.models import Incidente
from .models import Reporte
from .forms import ReporteForm
from base.mixins import RolRequeridoMixin


class ReporteHomeView(RolRequeridoMixin, TemplateView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Alta Gerencia']
    template_name = 'reports/reporte_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = Incidente.objects.filter(active=True)

        context['total_incidentes'] = qs.count()
        context['total_asi'] = qs.filter(estado_incidente__code='ASI').count()
        context['total_inv'] = qs.filter(estado_incidente__code='INV').count()
        context['total_cer'] = qs.filter(estado_incidente__code='CER').count()

        por_estado = qs.values(
            'estado_incidente__code', 'estado_incidente__name'
        ).annotate(total=Count('pk')).order_by('estado_incidente__code')
        context['por_estado'] = por_estado
        context['por_estado_max'] = por_estado.aggregate(m=Max('total'))['m'] or 1

        por_impacto = qs.values(
            'impacto_incidente__name'
        ).annotate(total=Count('pk')).order_by('-total')
        context['por_impacto'] = por_impacto
        context['por_impacto_max'] = por_impacto.aggregate(m=Max('total'))['m'] or 1

        por_tipo = qs.values(
            'tipo_incidente__name'
        ).annotate(total=Count('pk')).order_by('-total')
        context['por_tipo'] = por_tipo
        context['por_tipo_max'] = por_tipo.aggregate(m=Max('total'))['m'] or 1

        por_area = qs.values(
            'areas_afectadas__nombre'
        ).annotate(total=Count('pk')).order_by('-total')
        context['por_area'] = por_area
        context['por_area_max'] = por_area.aggregate(m=Max('total'))['m'] or 1

        context['ultimos_incidentes'] = qs.select_related(
            'estado_incidente', 'impacto_incidente', 'supervisor'
        ).order_by('-fecha_reportado')[:5]

        context['reportes'] = Reporte.objects.order_by('-created')[:5]

        return context


class ReporteListView(RolRequeridoMixin, ListView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Alta Gerencia']
    model = Reporte
    template_name = 'reports/reporte_list.html'
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reportes = self.object_list
        grupos = {}
        for r in reportes:
            key = r.tipo_reporte
            if key not in grupos:
                grupos[key] = {'label': r.get_tipo_reporte_display(), 'reportes': []}
            grupos[key]['reportes'].append(r)
        context['grupos_reporte'] = dict(sorted(grupos.items()))
        return context


class ReporteCreateView(RolRequeridoMixin, CreateView):
    roles_permitidos = ['Supervisor', 'Administrador']
    model = Reporte
    form_class = ReporteForm
    template_name = 'reports/reporte_form.html'
    success_url = reverse_lazy('reporte-lista')

    def form_valid(self, form):
        form.instance.generado_por = self.request.user.perfil_persona
        return super().form_valid(form)


class ReporteDetailView(RolRequeridoMixin, DetailView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Alta Gerencia']
    model = Reporte
    template_name = 'reports/reporte_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reporte = self.object
        qs = Incidente.objects.filter(active=True)

        if reporte.fecha_inicio:
            qs = qs.filter(fecha_reportado__date__gte=reporte.fecha_inicio)
        if reporte.fecha_fin:
            qs = qs.filter(fecha_reportado__date__lte=reporte.fecha_fin)

        tipo = reporte.tipo_reporte
        if tipo == 'EST':
            qs = qs.order_by('estado_incidente__code')
        elif tipo == 'IMP':
            qs = qs.order_by('impacto_incidente__name')
        elif tipo == 'TIP':
            qs = qs.order_by('tipo_incidente__name')

        context['incidentes'] = qs.select_related(
            'estado_incidente', 'impacto_incidente', 'tipo_incidente', 'supervisor'
        )[:100]

        por_estado = qs.values(
            'estado_incidente__code', 'estado_incidente__name'
        ).annotate(total=Count('pk')).order_by('estado_incidente__code')
        context['por_estado'] = por_estado
        context['por_estado_max'] = por_estado.aggregate(m=Max('total'))['m'] or 1

        por_impacto = qs.values(
            'impacto_incidente__name'
        ).annotate(total=Count('pk')).order_by('-total')
        context['por_impacto'] = por_impacto
        context['por_impacto_max'] = por_impacto.aggregate(m=Max('total'))['m'] or 1

        por_tipo = qs.values(
            'tipo_incidente__name'
        ).annotate(total=Count('pk')).order_by('-total')
        context['por_tipo'] = por_tipo
        context['por_tipo_max'] = por_tipo.aggregate(m=Max('total'))['m'] or 1

        return context


class IncidenteFichaView(RolRequeridoMixin, DetailView):
    roles_permitidos = ['Supervisor', 'Administrador', 'Especialista', 'Alta Gerencia']
    model = Incidente
    template_name = 'reports/incidente_ficha.html'
    context_object_name = 'incidente'

    def get_queryset(self):
        return Incidente.objects.filter(active=True)
