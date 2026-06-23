def get_areas_supervision(persona):
    try:
        config = persona.config_gerencia
    except:
        return []
    
    areas = []
    for area in config.areas_supervision.all():
        areas.extend(get_areas_recursivas(area))
    return areas

def get_areas_recursivas(area):
    areas = [area]
    for subarea in area.subareas.all():
        areas.extend(get_areas_recursivas(subarea))
    return areas