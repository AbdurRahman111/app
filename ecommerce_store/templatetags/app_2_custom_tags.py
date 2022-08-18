from django import template
from ..models import app_2_website_logo, Get_In_Touch, social_media

register = template.Library()


# reguler order count


@register.simple_tag
def get_last_logo_app2():
    logo_get = app_2_website_logo.objects.last()
    if logo_get:
        logo_url = logo_get.image.url
    else:
        logo_url = '/static/default-logo.png'
    return logo_url



@register.simple_tag
def get_in_touch_text():
    txt = Get_In_Touch.objects.last()
    if txt:
        whole_text = txt.Text
    else:
        whole_text = ""
    return whole_text


@register.simple_tag
def get_social_url():
    txt = social_media.objects.last()
    if txt:
        social_url = txt.Url
    else:
        social_url = ""
    return social_url