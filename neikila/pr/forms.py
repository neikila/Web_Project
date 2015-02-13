from pr.models import *
from django import forms
import datetime

class QuestionForm(forms.ModelForm):
		
		def __init__(self, *args, **kwargs):
				self.author = kwargs.pop('user', None)
				self.rating = 0
				super(QuestionForm, self).__init__(*args, **kwargs)
		
		def save(self, commit = True):
				obj = super(QuestionForm, self).save(commit = False)
				if commit:
					obj.author_id = self.author
					obj.pub_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
					obj.save()
				return obj

		class Meta:
				model = Question
				exclude = ('author', 'pub_date', 'rating', )

class AnswerForm(forms.ModelForm):
		
		def __init__(self, *args, **kwargs):
				self.author = kwargs.pop('user', None)
				self.question = kwargs.pop('question', None)
				self.rating = 0
				super(AnswerForm, self).__init__(*args, **kwargs)
		
		def save(self, commit = True):
				obj = super(AnswerForm, self).save(commit = False)
				if commit:
					obj.author_id = self.author
					obj.question_id = self.question
					obj.IsCorrect = 0
					obj.pub_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
					obj.save()
				return obj

		class Meta:
				model = Answer
				exclude = ('author', 'pub_date', 'rating', 'question', 'IsCorrect',)

class UserForm(forms.ModelForm):
		
		def __init__(self, *args, **kwargs):
				super(UserForm, self).__init__(*args, **kwargs)
		
		def save(self, commit = True):
				obj = super(UserForm, self).save(commit = False)
				if commit:
					#obj.author_id = self.author
					#obj.question_id = self.question
					#obj.IsCorrect = 0
					#obj.pub_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
					obj.save()
				return obj

		class Meta:
				model = User
				exclude = ()
