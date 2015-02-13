from optparse import make_option
from django.core.management.base import BaseCommand
from pr.models import Profile, Tag, Question, Answer
from django.contrib.auth.models import User
from django.db.models import Count

from django.core.cache import caches

memcached = caches['default']
    	#context['best_users'] = Profile.objects.all().values('nickname', 'rating')order_by('-rating')[0:5]
class Command(BaseCommand):
    
		def handle(self, *args, **kwargs):
			context = {}
			Pop_tags = []
			T = Tag.objects.all().values('tag_text', 'id').annotate(Count("question")).order_by('-question__count')[0:5]	
			for i in T:
				Pop_tags.append({'id': i['id'], 'tag_text': i['tag_text']})
			memcached.set('popular_tags', Pop_tags, 3600)
			Best_Us = []
			Pr = Profile.objects.all().values('id', 'nickname', 'rating').order_by('-rating')[0:5]
			for i in Pr:
				Best_Us.append({'id': i['id'], 'nickname': i['nickname']})
			memcached.set('best_users', Best_Us, 3600)
