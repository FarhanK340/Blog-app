from django import template

register = template.Library()

@register.filter(name='add_attributes')
def add_attributes(field, args):
    attrs = {}
    for arg in args.split(','):
        key, value = arg.split(":")
        attrs[key.strip()] = value.strip()
    return field.as_widget(attrs=attrs)