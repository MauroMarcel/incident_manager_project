from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Departamento, Clasificacion_Sistema, Criticidad
from .serializers import (
    DepartamentoSerializer,
    ClasificacionSistemaSerializer,
    CriticidadSerializer
)


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la entidad Departamento.
    
    Proporciona operaciones CRUD completas:
    - GET /api/departamentos/ - Lista todos los departamentos
    - POST /api/departamentos/ - Crea un nuevo departamento
    - GET /api/departamentos/{id}/ - Obtiene un departamento específico
    - PUT /api/departamentos/{id}/ - Actualiza un departamento
    - PATCH /api/departamentos/{id}/ - Actualización parcial
    - DELETE /api/departamentos/{id}/ - Elimina un departamento
    """
    
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['active', 'code']
    search_fields = ['name', 'code', 'centro_costo']
    ordering_fields = ['name', 'code', 'created']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtiene solo los departamentos activos"""
        departamentos = self.queryset.filter(active=True)
        serializer = self.get_serializer(departamentos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivos(self, request):
        """Obtiene solo los departamentos inactivos"""
        departamentos = self.queryset.filter(active=False)
        serializer = self.get_serializer(departamentos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activa un departamento específico"""
        departamento = self.get_object()
        departamento.active = True
        departamento.save()
        serializer = self.get_serializer(departamento)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """Desactiva un departamento específico"""
        departamento = self.get_object()
        departamento.active = False
        departamento.save()
        serializer = self.get_serializer(departamento)
        return Response(serializer.data)


class ClasificacionSistemaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la entidad Clasificacion_Sistema.
    
    Proporciona operaciones CRUD completas:
    - GET /api/clasificaciones/ - Lista todas las clasificaciones
    - POST /api/clasificaciones/ - Crea una nueva clasificación
    - GET /api/clasificaciones/{id}/ - Obtiene una clasificación específica
    - PUT /api/clasificaciones/{id}/ - Actualiza una clasificación
    - PATCH /api/clasificaciones/{id}/ - Actualización parcial
    - DELETE /api/clasificaciones/{id}/ - Elimina una clasificación
    """
    
    queryset = Clasificacion_Sistema.objects.all()
    serializer_class = ClasificacionSistemaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['active', 'code']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'created']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Obtiene solo las clasificaciones activas"""
        clasificaciones = self.queryset.filter(active=True)
        serializer = self.get_serializer(clasificaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivas(self, request):
        """Obtiene solo las clasificaciones inactivas"""
        clasificaciones = self.queryset.filter(active=False)
        serializer = self.get_serializer(clasificaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activa una clasificación específica"""
        clasificacion = self.get_object()
        clasificacion.active = True
        clasificacion.save()
        serializer = self.get_serializer(clasificacion)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """Desactiva una clasificación específica"""
        clasificacion = self.get_object()
        clasificacion.active = False
        clasificacion.save()
        serializer = self.get_serializer(clasificacion)
        return Response(serializer.data)


class CriticidadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la entidad Criticidad.
    
    Proporciona operaciones CRUD completas:
    - GET /api/criticidades/ - Lista todas las criticidades
    - POST /api/criticidades/ - Crea una nueva criticidad
    - GET /api/criticidades/{id}/ - Obtiene una criticidad específica
    - PUT /api/criticidades/{id}/ - Actualiza una criticidad
    - PATCH /api/criticidades/{id}/ - Actualización parcial
    - DELETE /api/criticidades/{id}/ - Elimina una criticidad
    """
    
    queryset = Criticidad.objects.all()
    serializer_class = CriticidadSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['active', 'code']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'created']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Obtiene solo las criticidades activas"""
        criticidades = self.queryset.filter(active=True)
        serializer = self.get_serializer(criticidades, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactivas(self, request):
        """Obtiene solo las criticidades inactivas"""
        criticidades = self.queryset.filter(active=False)
        serializer = self.get_serializer(criticidades, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activa una criticidad específica"""
        criticidad = self.get_object()
        criticidad.active = True
        criticidad.save()
        serializer = self.get_serializer(criticidad)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """Desactiva una criticidad específica"""
        criticidad = self.get_object()
        criticidad.active = False
        criticidad.save()
        serializer = self.get_serializer(criticidad)
        return Response(serializer.data)
