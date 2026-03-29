"""
Script para desactivar algunas personas para pruebas.
Ejecutar con: python manage.py shell < data_seed.py
"""
from users.models import Persona

# Obtener todas las personas
personas = Persona.objects.all()[:5]  # Tomar las primeras 5

# Desactivar la mitad
for i, persona in enumerate(personas):
    if i % 2 == 0:  # Desactivar cada segunda persona
        persona.active = False
        persona.save()
        print(f"✓ Desactivado: {persona.nombre} {persona.apellidos}")
    else:
        persona.active = True
        persona.save()
        print(f"✓ Activado: {persona.nombre} {persona.apellidos}")

print("\n✅ Datos de prueba actualizados")
