from django import template
from ..models import website_logo, Get_In_Touch_app_3, social_media_app_3

register = template.Library()


# reguler order count


@register.simple_tag
def get_last_logo_app3():
    logo_get = website_logo.objects.last()
    if logo_get:
        logo_url = logo_get.image.url
    else:
        logo_url = '/static/default-logo.png'
    return logo_url



@register.simple_tag
def get_in_touch_text_app3():
    txt = Get_In_Touch_app_3.objects.last()
    if txt:
        whole_text = txt.Text
    else:
        whole_text = ""
    return whole_text


@register.simple_tag
def get_social_url_app3():
    txt = social_media_app_3.objects.last()
    if txt:
        social_url = txt.Url
    else:
        social_url = ""
    return social_url