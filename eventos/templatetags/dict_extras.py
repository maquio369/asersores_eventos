from django import template

register = template.Library()

@register.filter(name='dictkey')
def dictkey(d, key):
    """Permite acceder a una clave de diccionario en la plantilla"""
    return d.get(key)
