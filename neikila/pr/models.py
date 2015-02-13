from django.db import models
from django.contrib.auth.models import User
from djangosphinx.models import SphinxSearch

class Profile(models.Model):
	user = models.OneToOneField(User)
	rating = models.IntegerField(default = 0)
	avatar = models.CharField(max_length = 40)
	nickname = models.CharField(max_length = 40, default = 'nickname')


class Question(models.Model):
	question_text = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date published')
	header = models.CharField(max_length = 50)
	rating = models.IntegerField(default = 0)
	author = models.ForeignKey(User, default = 1)

	search = SphinxSearch(
		index = 'pr_question_index',
		weights = {	'header': 100, 'question_text': 50}
	)

	def __str__(self):
			return self.question_text + self.header + str(self.pub_date) + str(self.rating) + str(self.author) 


class Answer(models.Model):
	question = models.ForeignKey(Question, related_name = 'answers')
	answer_text = models.CharField(max_length = 400)
	pub_date = models.DateTimeField('date publiched')
	IsCorrect = models.IntegerField(default = 0)
	author = models.ForeignKey(User, default = 1)
	rating = models.IntegerField(default = 0)


class Tag(models.Model):
	question = models.ManyToManyField(Question)
	tag_text = models.CharField(max_length = 30)

class VoteForPosts(models.Model):
	value = models.IntegerField()
	voter = models.ForeignKey(User, related_name = 'VoteForPost')
	post = models.IntegerField(default = 0)
	p_type = models.IntegerField(default = 0) #0 - Question, 1 - Answer

