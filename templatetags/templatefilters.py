from django.template

register = Library()

@register.filter()
def is_false(arg):
	return arg is False

@register.filter()
def to_int(value):
	value = float(value)
	return int(value)

@register.filter()
def get_item(dictonary, key):
	val = key
	return val

@register.filter()
def to_upper(value):
	value = value.upper()
	return value