from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from recipe_list.models import RecipeModel, CommentModel, LikesCommentModel
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings

@login_required
def updateComment(request):
	"""
	Представления запроса на получение списка комментариев.
	Доступ к запросу имеют только авторизированные пользователи.
	Обрабатывает GET запрос.
	Данные:
		recipe_id(int): id рецепта, комментарии к которому нужно получить.
		count_comments(int): кол-во комментраиев, которое нужно получить
	Возврашает HTML с комментариями
	"""
	count = int(request.GET.get('count_comments'))
	recipe_id = int(request.GET.get('recipe_id'))
	
	comment_cache = cache.get(f'{settings.COMMENTS_LIST_NAME}:{recipe_id}')
	if comment_cache:
		result = comment_cache[:count]
	else:
		recipe = RecipeModel.objects.get(id=recipe_id)
		data_comment = CommentModel.objects.filter(recipe = recipe).order_by('-data_create')
		result = []
		for item in data_comment:
			count_likes = len(LikesCommentModel.objects.filter(comment = item))
			if count_likes > 99999999:
				count_likes = str(count_likes // 100000000) +'kkk'
			elif count_likes > 99999:
				count_likes = str(count_likes // 100000) +'kk'
			elif count_likes > 999:
				count_likes = str(count_likes // 1000) +'k'
			result.append({'comment': item, 'likes': count_likes})
		cache.set(f'{settings.COMMENTS_LIST_NAME}:{recipe_id}', result, settings.COMMENTS_LIST_TTL)
		result = result[:count]

	return render(request, 'comments_update.html', {'data': result})

@login_required
def newLike(request):
	"""
	Добавление нового лайка.
	Доступ к запросу имеют только авторизированные пользователи.
	Обрабатывает POST запрос.
	Данные:
		id_comment(int): id комментария, на который ставят лайк.
	Возвращает информаци о обновление данных
	"""
	id_comment = request.POST.get('id_comment')
	comment_obj = CommentModel.objects.get(id=id_comment)
	old_like = LikesCommentModel.objects.filter(
			owner = request.user,
			comment = comment_obj
		)
	cache.delete(f'{settings.COMMENTS_LIST_NAME}:{comment_obj.recipe.id}')
	if len(old_like) > 0: #Удаление лайка, если он уже был.
		old_like.delete()
		return JsonResponse({'res': True, "data":"Лайк был удален, так как был ранее поставлен от этого пользователя"}, status=200)
	else: #добавления лайка
		LikesCommentModel.objects.create(
				owner = request.user,
				comment = comment_obj
			)
		return JsonResponse({'res': True, "data":"Лайк был поставлен"}, status=201)

@login_required
def deleteComment(request):
	'''
	Удаление комментария.
	Доступ к запросу имеют только авторизированные пользователи.
	Обрабатывает POST запрос.
	Данные:
		id_comment(int): id комментария, который подлежит удалению.
	Возвращает информаци о обновление данных
	'''
	id_comment = request.POST.get('id_comment')
	comm_to_delete = CommentModel.objects.get(id=id_comment)
	if comm_to_delete.owner == request.user:
		cache.delete(f'{settings.COMMENTS_LIST_NAME}:{comm_to_delete.recipe.id}')
		comm_to_delete.delete()
		return JsonResponse({'res': True, "data":"Комментарий был удален"}, status=200)
	return JsonResponse({'res': False, "data":"Это не Ваш комментарий"}, status=403)

@login_required
def newComment(request):
	'''
	Добавление нового комментария
	Доступ к запросу имеют только авторизованные пользователи
	Обрабатывает POST запрос
	Данные:
		recipe_id(int): id рецепта, которому добавить комментарий
		text(str): текст комментария
	'''	
	text = request.POST.get('text')
	recipe_id = int(request.POST.get('recipe_id'))
	if text == "":
		return JsonResponse({'res': False, "data":"Комментарий пустой"}, status=400)
	cache.delete(f'{settings.COMMENTS_LIST_NAME}:{recipe_id}')
	CommentModel.objects.create(
			owner = request.user,
			recipe = RecipeModel.objects.get(id=recipe_id),
			comment = text
		)
	return JsonResponse({'res': True, "data":"Комментарий добавлен"}, status=201)