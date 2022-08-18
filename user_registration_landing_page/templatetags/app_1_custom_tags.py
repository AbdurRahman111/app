from django import template
from ..models import app_1_website_logo, Get_In_Touch_app1, social_media_app1

register = template.Library()

@register.simple_tag
def get_last_logo_app1():
    logo_get = app_1_website_logo.objects.last()
    if logo_get:
        logo_url = logo_get.image.url
    else:
        logo_url = '/static/default-logo.png'
    return logo_url

@register.simple_tag
def get_in_touch_text_app1():
    txt = Get_In_Touch_app1.objects.last()
    if txt:
        whole_text = txt.Text
    else:
        whole_text = ""
    return whole_text

@register.simple_tag
def get_social_url_app1():
    txt = social_media_app1.objects.last()
    if txt:
        social_url = txt.Url
    else:
        social_url = ""
    return social_url