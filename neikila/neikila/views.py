from django.http import HttpResponse
#from django.http import QueryDict
from django.shortcuts import render, redirect
from pr.models import *
import os
import re
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404

from neikila.settings import *
from pr.forms import *

from django.contrib.auth.decorators import login_required

def index(req, sort='new', profile_id = 0):
    context = { }
    order = sort == 'hot' and '-rating' or '-pub_date'
    if profile_id == 0:
        context['title'] = "Best Questions"
        queryset = Question.objects.all().values('id', 'question_text', 'rating', 'header', 'pub_date', 'author_id__profile__avatar', 'author_id__profile__nickname').annotate(Count("answers")).order_by(order)
    else:
        context['title'] = "Your Questions"
        queryset = Question.objects.all().values('id', 'question_text', 'rating', 'header', 'pub_date', 'author_id__profile__avatar', 'author_id__profile__nickname').annotate(Count("answers")).order_by(order).filter(author_id = profile_id)
    limit = 5;
    pager = Paginator(queryset, limit);
    page = req.GET.get('page', 1)
    context['page'] = page
    try:
        context['queryset'] = pager.page(page)
    except EmptyPage:
        page = pager.num_pages	
        context['page'] = page
        context['queryset'] = pager.page(page)
    context['minPageNumber'] = int(page) - 5
    context['maxPageNumber'] = int(page) + 5
    context['question'] = pager.page(page).object_list
    context['pager'] = pager
    context['tags'] = Question.objects.all().values('id', 'tag__tag_text')
    context['popular_tags'] = Tag.objects.all().values('tag_text').annotate(Count("question")).order_by('-question__count')[0:5]	
    context['best_users'] = User.objects.all().order_by('-profile__rating')[0:5]
    return render(req, 'index.html', context)

def answers(req): 
	context = { }
	q_id = req.GET.get('q_id', 1)
        if req.method == 'POST':
                form = AnswerForm(req.POST, user = req.user.id, question = q_id)
                if form.is_valid():
                    ob = form.save()
                    link = '/answer?q_id=' + str(q_id)
                    return redirect(link)
        else:
            context['form'] = AnswerForm()
	    context['q_id'] = q_id
	    context['question'] = Question.objects.all().values('id', 'question_text', 'rating', 'header', 'pub_date', 'author_id__profile__nickname', 'author_id__profile__avatar').filter(id=q_id)
	    queryset = Answer.objects.all().values('id', 'answer_text', 'IsCorrect', 'author_id__profile__nickname', 'author_id', 'pub_date', 'rating', 'author_id__profile__avatar').filter(question_id = q_id).order_by('pub_date')
	    limit = 5
	    pager = Paginator(queryset, limit)
	    page = req.GET.get('page', 1)
	    try:
    	    	context['queryset'] = pager.page(page)
	    except EmptyPage:
    		page = pager.num_pages	
    		context['page'] = page
	    	context['queryset'] = pager.page(page)
	    context['minPageNumber'] = int(page) - 5
	    context['maxPageNumber'] = int(page) + 5
	    context['answers'] = pager.page(page).object_list
	    context['page'] = pager
	    context['tags'] = Question.objects.filter(id = q_id).values('tag__tag_text')
	    context['popular_tags'] = Tag.objects.all().values('tag_text').annotate(Count("question")).order_by('-question__count')[0:5]	
	    context['best_users'] = User.objects.all().order_by('-profile__rating')[0:5]
	    return render(req, 'answers.html', context)



@login_required
def like(req):
        pk = req.POST.get('id')
        mark = int(req.POST.get('mark'))
        ptype = int(req.POST.get('ptype'))
        p_change = "#q" + str(pk)
        if ptype == 0:
            p_change = "#q" + str(pk)
        else:
            p_change = "#a" + str(pk)
        new_rate = '0'
        status = False
        try:
            if ptype == 0:
                p = Question.objects.get(id = pk)
            else:
                p = Answer.objects.get(id = pk)
            new_rate = str(p.rating)
            if p.author_id != req.user.id:
                Vote = VoteForPosts.objects.filter(p_type = ptype).filter(post = pk).filter(voter_id = req.user.id)
                if Vote.count() != 0:
                    vote_last = Vote[0].value
                else:
                    vote_last = 0
                if mark * vote_last != 1:
                    Pr = Profile.objects.get(id = p.author_id)
                    Pr.rating += mark
                    Pr.save()
                    p.rating = p.rating + mark
                    if vote_last != 0:
                        Vote[0].delete()
                    else:
                        Vote = VoteForPosts(post = pk, voter_id = req.user.id, value = mark, p_type = ptype)
                        Vote.save()
                    message = 'Thanks for your vote!'
                    p.save()
                else:
                    message = 'You cant`t make a double vote!'
                status = True
                new_rate = str(p.rating)
            else:
                message = 'You are not permitted to vote your post!'
        except:
            message = p_change
        import json
        content =json.dumps({'status': status, 'q_change': p_change , 'message': message, 'new_rating': new_rate})

        return HttpResponse(content, content_type = 'application/json')


@login_required
def profile(req):
        return index(req, 'new', req.user.id)

@login_required
def settings(req):
	context = { }
        return render(req, 'settings.html', context)

def handle_uploaded_file(up_file):
        destination = open(BASE_DIR + '/uploads/' + 'avatar/' + up_file.name, 'w+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        destination.close()

@login_required
def save(req):
	context = { }
        context['Wrong_email'] = False
        context['Email_is_busy'] = False
        context['Wrong_len'] = False
        context['Nickname_is_busy'] = False
        if (req.method == 'POST'):
            Pr = Profile.objects.get(id = req.user.id)
            U = User.objects.get(id = req.user.id)
            try:
                route = req.FILES['avatar'].name
                handle_uploaded_file(req.FILES['avatar'])
                Pr.avatar = "/" + route
            except: 
                route = 0
            try:
                mail = req.POST['email']
                if len(mail) > 0:
                    p = re.compile('^[a-zA-Z0-9]{3,}\@[a-zA-Z]{2,}\.[a-z]{2,}$', re.U)
                    if p.search(mail) and User.objects.filter(email = mail) == 0:
                        U.email = mail
                    else:
                        if p.search(mail) is None:
                            context['Wrong_email'] = True
                        else:
                            context['Email_is_busy'] = True
            except:
                mail = 0
                
            try:
                nick = req.POST['nickname']
                if len(nick) > 0:
                    if len(nick) > 3 and Profile.objects.filter(nickname = nick) == 0 and len(nick) > 40:
                        Pr.nickname = nick
                    else:
                        if len(nick) < 4 or len(nick) > 40:
                            context['Wrong_len'] = True
                        else:
                            context['Nickname_is_busy'] = True

            except: 
                nickname = 0
            Pr.save()
            U.save()
            if context['Nickname_is_busy'] or context['Wrong_len'] or context['Email_is_busy'] or context['Wrong_email']:
                context['Error'] = True
            else:
                context['Error'] = False
        return render(req, 'settings.html', context)


@login_required
def ask_question(req):
        if req.method == 'POST':
                form = QuestionForm(req.POST, user = req.user.id)
                if form.is_valid():
                    ob = form.save()
                    link = '/answer?q_id=' + str(ob.id)
                    return redirect(link)
        else:
            form = QuestionForm()
        return render(req, 'ask_question.html', {'form': form})


from django.contrib.auth.forms import UserCreationForm

def signin(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/")
	else:
		form = UserCreationForm()
	return render(request, "registration/register.html", {'form' : form})


def search(req):
    context = { }
    query = req.GET.get('query')
    queryset = Question.search.query(query).order_by('@weight')
    limit = 5;
    pager = Paginator(queryset, limit);
    page = req.GET.get('page', 1)
    context['page'] = page
    try:
        context['queryset'] = pager.page(page)
    except EmptyPage:
        page = pager.num_pages	
        context['page'] = page
        context['queryset'] = pager.page(page)
    context['minPageNumber'] = int(page) - 5
    context['maxPageNumber'] = int(page) + 5
    context['question'] = pager.page(page).object_list
    context['pager'] = pager
    context['tags'] = Question.objects.all().values('id', 'tag__tag_text')
    context['popular_tags'] = Tag.objects.all().values('tag_text').annotate(Count("question")).order_by('-question__count')[0:5]	
    context['best_users'] = User.objects.all().order_by('-profile__rating')[0:5]
    return render(req, 'search.html', context)
		

def test2(request):
	output = "<html> "
	output = output + "<head> "
	output = output + "<title>Title List Apach </title> "
	output = output + "</head> "
	output = output + "<body bgcolor=silver teext=black> "
	output = output + "<h2>MHTC Bauman</h2><br> "
	output = output + "<h3>Faculty SAPR</h3><br><br><br> "
	output = output + "<div align=center> "
	output = output + "Examination work<br> "
	output = output + 'disciple "Developing OS"<br><br> '
	output = output + 'Theme "Market" '
	output = output + "</div> "
	output = output + "<div align=left> "
	output = output + "Student Ivanov<br> "
	output = output + "Group Rk6-52 "
	output = output + "</div> "
	output = output + "</body> "
	output = output + "</html> "
	return HttpResponse(output)

#def ask_qiestion(request):
#    if request.method == 'POST'
#        form = QuestionForm(request.Post, user = request.user)
#        if form.is_Valid():
#            form.save()
#            return redirrect('/')
#    else:
#        form = QuestionForm()
#    return render(request, 'ask.html', { 'form' : form })

