from django import template
from django.core.cache import caches

register = template.Library()
memcached = caches['default']

@register.inclusion_tag("incl/pop_tags.html")
def best_tags():
    context = { }
    context['popular_tags'] = memcached.get('popular_tags')#Tag.objects.all().values('tag_text').annotate(Count("question")).order_by('-question__count')[0:5]	
    return context


@register.inclusion_tag("incl/cool_users.html")
def best_users():
    context = { }
    context['best_users'] = memcached.get('best_users') #Profile.objects.all().values('nickname', 'rating')order_by('-rating')[0:5]
    return context
