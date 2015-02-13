from optparse import make_option
from django.core.management.base import BaseCommand
from pr.models import Profile, Tag, Question, Answer
from django.contrib.auth.models import User

from faker.frandom import random
from faker.lorem import sentence, sentences
from mixer.fakers import get_email
from mixer.fakers import get_genre
from mixer.fakers import get_username
from pprint import pformat
from django.db.models import Min, Max

import string, time

def time_for_model(start = "20000328060000"):
        start_date_time_in_python_format = time.strptime(start ,"%Y%m%d%H%M%S")
        start_date_time_in_seconds = time.mktime(start_date_time_in_python_format)
        finish_date_time_in_python_format = time.strptime("20200328060000","%Y%m%d%H%M%S")
        finish_date_time_in_seconds = time.mktime(finish_date_time_in_python_format)
        random.seed()
        seconds_to_time = random.randrange(start_date_time_in_seconds, finish_date_time_in_seconds, 851);
        seconds_to_time = time.localtime(seconds_to_time)
        time_to_string = time.strftime("%Y-%m-%d %H:%M:%S", seconds_to_time)
        return time_to_string

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
			make_option('--users',
				action='store',
				dest='users',
				default=0,
				),
			make_option('--tags',
				action='store',
				dest='tags',
				default=0,
				),
			make_option('--questions',
				action='store',
				dest='questions',
				default=0,
				),
			make_option('--answers',
				action='store',
				dest='answers',
				default=0,
				),
			)


	def handle(self, *args, **options):
		names = {}
		while(len(names.keys()) < int(options['users'])):
			names[get_username(length=20)] = 1
		for name in names.keys():
			u = User.objects.create(username=name, email = get_email())
			p = Profile.objects.create(user_id = u.id, rating = random.randint(0,20), avatar = "/jpeg/a.jpeg")
			u.set_password('WebProject')
			u.save()

		for i in range(0, int(options['tags'])):
			t = Tag.objects.create(tag_text = get_genre())

		tag_min = Tag.objects.all().aggregate(Min('id'))['id__min']
		tag_max = Tag.objects.all().aggregate(Max('id'))['id__max']
		
		p_min = Profile.objects.all().aggregate(Min('id'))['id__min']
		p_max = Profile.objects.all().aggregate(Max('id'))['id__max']
		for i in range(0, int(options['questions'])):
			q = Question.objects.create(author_id = random.randint(p_min, p_max), header = (sentence())[0:20], question_text = sentences(3), pub_date = time_for_model(), rating = random.randint(-999, 999))
			tag_amount = random.randint(3, 5)
			for j in range(0, tag_amount):
				t = Tag.objects.get(id = random.randint(tag_min, tag_max))
				t.question.add(q)
				t.save()

		q_min = Question.objects.all().aggregate(Min('id'))['id__min']
		q_max = Question.objects.all().aggregate(Max('id'))['id__max']
		if int(options['answers']) != 0:
			for i in range(q_min, q_max):
				try:
					q = Question.objects.get(id = i)
				except:
					continue
				count = Answer.objects.filter(question_id = i).count()
				ans_max = 50
				if count > 15:
					ans_max = 40
				if count > 30:
					ans_max = 20
				if count > 50:
					ans_max = 10
				if ans_max > int(options['answers']):
					ans_max = int(options['answers'])
				ans_amount = random.randint(1, ans_max)
				for j in range(0, ans_amount):
					auth_id = random.randint(p_min, p_max)
					date = time_for_model(q.pub_date.strftime("%Y%m%d%H%M%S"))
					a = Answer.objects.create(question = q, answer_text = sentences(4), pub_date = date, IsCorrect = 0, author_id = auth_id, rating = random.randint(-999,999))



"""
 def FillDB(req):
        return index(req)
def FillDB(req):
        random.seed()
        # Users

        for i in range(1, 30):
            size = random.randrange(8, 20)
            nick = ""
            for i in xrange(size):
                nick = nick + nick.join(random.choice(string.letters))
            size = random.randrange(8, 20)
            mail = "temp@gmail.com"
            date = time_for_model()
            size = random.randrange(8, 20)
            passw = ""
            for i in xrange(size):
                passw = passw + passw.join(random.choice(string.letters))
            rate = random.randrange(-1000, 1000) 
            route = "/jpeg/a.jpeg"
            q = User(nickname = nick, email = mail, DOR = date, password = passw, rating = rate, avatar = route)
            q.save()
        # Questions 
        for i in range(1, 30):
            size = random.randrange(20, 100)
            text = ""
            count = 0
            spacestop = random.randrange(3,14)
            for i in xrange(size):
                count = count + 1
                if (count == spacestop):
                    count = 0
                    spacestop = random.randrange(3,14)
                    text = text + text.join(" ")
                text = text + text.join(random.choice(string.letters))
            date = time_for_model()
            size = random.randrange(5, 30)
            head = ""
            count = 0
            spacestop = random.randrange(3,14)
            for i in xrange(size):
                count = count + 1
                if (count == spacestop):
                    count = 0
                    spacestop = random.randrange(3,14)
                    head = head + head.join(" ")
                head = head + head.join(random.choice(string.letters))
            rate = random.randrange(-1000, 1000) 
            au = random.randrange(1, 6)
            au = User.objects.all().get(id=au)
            q = Question(question_text = text, pub_date = date, header = head, rating = rate, author = au)
            q.save()
        # Answers
        #for i in Question.objects.all():
        #    text = ""
        #    count = 0
        #    spacestop = random.randrange(3,14)
        #    for i in xrange(size):
        #        count = count + 1
        #        if (count == spacestop):
        #            count = 0
        #            spacestop = random.randrange(3,14)
        #            text = text + text.join(" ")
        #        text = text + text.join(random.choice(string.letters))
        return index(req)

""" 
