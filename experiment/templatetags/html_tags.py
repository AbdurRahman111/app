import os
import codecs
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def read_html_file(html_field):
    print('File: ',html_field)
    html_path = html_field.path
    if os.path.exists(html_path):
        html_string = codecs.open(html_path, 'r').read()
        return mark_safe(html_string)
    return None
