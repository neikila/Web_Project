
	search = SphinxSearch({
		'index': 'pr_question_index',
		'weights': {
			'header': 100,
			'question_text': 50,
			},
	})

    context = { }
		query = req.GET.get('query')
    queryset = Question.search.query('query').values('id', 'question_text', 'rating', 'header', 'pub_date', 'author_id__profile__avatar', 'author_id__profile__nickname').annotate(Count("answers")).order_by('-pub_date')
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

@login_required
def like(req):
        pk = req.POST.get('id')
        mark = int(req.POST.get('mark'))
        q_change = "#q" + str(pk)
        new_rate = '0'
        status = False
        try:
            q = Question.objects.get(id = pk)
            new_rate = str(q.rating)
            if q.author_id != req.user.id:
                Vote = VoteForPosts.objects.filter(post_id = pk).filter(voter_id = req.user.id)
                if Vote.count() != 0:
                    vote_last = Vote[0].value
                else:
                    vote_last = 0
                if mark * vote_last != 1:
                    q.rating = q.rating + mark
                    if vote_last != 0:
                        Vote[0].delete()
                    else:
                        Vote = VoteForPosts(post_id = pk, voter_id = req.user.id, value = mark)
                        Vote.save()
                    message = 'Thanks for your vote!'
                    q.save()
                else:
                    message = 'You cant`t make a double vote!'
                status = True
                new_rate = str(q.rating)
            else:
                message = 'You are not permitted to vote your post!'
        except:
            message = q_change
        import json
        content =json.dumps({'status': status, 'q_change': q_change , 'message': message, 'new_rating': new_rate})

        return HttpResponse(content, content_type = 'application/json')
@login_required
def like(req):
        pk = req.POST.get('id')
        mark = int(req.POST.get('mark'))
        ptype = int(req.POST.get('ptype'))
        if ptype == 0:
            p_change = "#q" + str(pk)
        else:
            p_change = "#a" + str(pk)
        new_rate = '0'
        status = False
        p = Question.objects.get(id = -100)
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
                    p.rating = p.rating + mark
                    if vote_last != 0:
                        Vote[0].delete()
                    else:
                        Vote = VoteForPosts(post = pk, voter_id = req.user.id, value = mark)
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
