from rest_framework import serializers
from .models import Departamento, Clasificacion_Sistema, Criticidad


class DepartamentoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Departamento"""
    
    class Meta:
        model = Departamento
        fields = [
            'id',
            'code',
            'name',
            'centro_costo',
            'active',
            'created',
            'updated'
        ]
        read_only_fields = ['id', 'created', 'updated']


class ClasificacionSistemaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Clasificacion_Sistema"""
    
    class Meta:
        model = Clasificacion_Sistema
        fields = [
            'id',
            'code',
            'name',
            'active',
            'created',
            'updated'
        ]
        read_only_fields = ['id', 'created', 'updated']


class CriticidadSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Criticidad"""
    
    class Meta:
        model = Criticidad
        fields = [
            'id',
            'code',
            'name',
            'active',
            'created',
            'updated'
        ]
        read_only_fields = ['id', 'created', 'updated']
