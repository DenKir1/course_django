from django import template

register = template.Library()


@register.filter()
def mediapath(values):
    if values:
        return f'/media/{values}'


@register.simple_tag
def mediapath(values):
    if values:
        return f'/media/{values}'


@register.simple_tag
def like_count(values):
    if values:
        values = + 1
        return f'{values}'