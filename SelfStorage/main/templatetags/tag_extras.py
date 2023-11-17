from django import template

register = template.Library()


@register.filter(name='to_meters')
def to_meters(value: int):
    return value/100


@register.filter(name="to_sqm")
def to_square_meters(width: int, length: int):
    return width*length/100
