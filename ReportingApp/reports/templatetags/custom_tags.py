from django import template
register = template.Library()


@register.filter(name='index')
def index(List, i):
    if i < len(List):
        return List[int(i)]
    return ''

@register.filter(name='addclass')
def addclass(field, css):
   return field.as_widget(attrs={"class":css})