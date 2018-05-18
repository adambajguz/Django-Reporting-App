from django import template
register = template.Library()


@register.filter(name='index')
def index(List, i):
    if i < len(List):
        return List[int(i)]
    return ''

@register.simple_tag(name='define')
def define(val=None):
  return val

@register.simple_tag(name='define_global_in_context', takes_context=True)
def define_global_in_context(context, key, value):
    """
    Sets a value to the global template context, so it can
    be accessible across blocks.

    Note that the block where the global context variable is set must appear
    before the other blocks using the variable IN THE BASE TEMPLATE.  The order
    of the blocks in the extending template is not important. 

    Usage::
        {% extends 'base.html' %}

        {% block first %}
            {% set_global_context 'foo' 'bar' %}
        {% endblock %}

        {% block second %}
            {{ foo }}
        {% endblock %}
    """
    context.dicts[0][key] = value
    return ''