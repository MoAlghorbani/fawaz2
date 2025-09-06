from django import template
import os

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """
    Template filter to lookup a value in a dictionary by key.
    Usage: {{ dict|lookup:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def basename(path):
    """
    Template filter to get the basename of a file path.
    Usage: {{ file_path|basename }}
    """
    if path:
        return os.path.basename(str(path))
    return ''