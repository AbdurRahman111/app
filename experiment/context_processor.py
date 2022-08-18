from django.urls import resolve

def get_common_context(request):
    return {'app_name': resolve(request.path).app_name}