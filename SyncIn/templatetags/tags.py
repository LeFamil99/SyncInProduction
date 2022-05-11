from django import template

register = template.Library()

@register.simple_tag
def user(request):
    if request.user.is_authenticated:
        is_connected = True
    else:
        is_connected = False
    return is_connected