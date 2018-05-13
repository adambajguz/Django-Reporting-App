from django import template
register = template.Library()

@register.filter
def index(List, i):
    if i < len(List):
        return List[int(i)]
    return ''
