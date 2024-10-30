from django.shortcuts import render, redirect, HttpResponse
from recipe_list.models import RecipeModel, CommentModel, LikesCommentModel,SavedRecipeModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from recipe_list.forms import EditRecipeForm, SaveRecipeForm
from django.conf import settings
import re
from django.core.cache import cache
from django.conf import settings
from recipe_list.tasks import newRecipe, updateRecipe

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def home(request):
	"""
	Представление, которое обрабатывает главную страницу сайта и возвращает список всех рецептов.
	При получение POST запроса, применяются сортировка отображения данных по параметрам:
		recipes_need(int): кол-во рецептов для выдачи
		search_name(str): часть имени по которому будет происходить поиск элементов
		category_data(str): категория блюд для выдачи
		sort_by(str): сортировка по по пулярности или времени добавляния (popular/time)
	"""
	recipe_cache = cache.get(f"{settings.RECIPE_LIST_NAME}")
	if recipe_cache:
		all_recipe = recipe_cache
	else:
		all_recipe = RecipeModel.objects.all()
		cache.set(f"{settings.RECIPE_LIST_NAME}", all_recipe, settings.RECIPE_LIST_TTL)

	if request.method == 'POST':
		count_recipe = int(request.POST.get('recipes_need'))
		name_search = request.POST.get('search_name')
		category_data = request.POST.get('category_data')
		sort = request.POST.get('sort_by')
		if sort == 'popular':
			list_recipe = all_recipe.filter(title__icontains = name_search, category__icontains=category_data).order_by('-count_view')[:count_recipe] #icontains без учета регистра
		else:
			list_recipe = all_recipe.filter(title__icontains = name_search, category__icontains=category_data).order_by('-data_create')[:count_recipe] #минус перед сортировкой это чтобы перевернуть
		return render(request, 'new_recipe.html',{'data': list_recipe})
	list_recipe = all_recipe.order_by('-count_view')[:settings.START_COUNT_VIEW]
	return render(request, 'index.html',{'data': list_recipe, 'sort_list': settings.CATEGORY_LIST})

def recipeByUser(request, user_id: int):
	"""
	Обработчик отображения страницы рецептов, который добавил пользователь.
	Параметры:
		user_id(int): это id пользователя, страницу которого нужно открыть
	При получение POST запроса, применяются сортировка отображения данных по параметрам:
		recipes_need(int): кол-во рецептов для выдачи
		search_name(str): часть имени по которому будет происходить поиск элементов
		category_data(str): категория блюд для выдачи
		sort_by(str): сортировка по по пулярности или времени добавляния (popular/time)
	"""
	recipe_cache = cache.get(f"{settings.RECIPE_LIST_NAME}")
	if recipe_cache:
		all_recipe = recipe_cache
	else:
		all_recipe = RecipeModel.objects.all()
		cache.set(f"{settings.RECIPE_LIST_NAME}", all_recipe, settings.RECIPE_LIST_TTL)
	users_cache = cache.get(f"{settings.USER_OBJS_NAME}:{user_id}")
	if users_cache:
		user = users_cache
	else:
		user = get_user_model().objects.get(id=user_id)
		cache.set(f"{settings.USER_OBJS_NAME}:{user_id}", user, settings.USER_OBJS_TTL)
	if request.method == 'POST':
		count_recipe = int(request.POST.get('recipes_need'))
		name_search = request.POST.get('search_name')
		category_data = request.POST.get('category_data')
		sort = request.POST.get('sort_by')
		if sort == 'popular':
			list_recipe = all_recipe.filter(title__icontains = name_search, category__icontains=category_data, owner=user).order_by('-count_view')[:count_recipe] #icontains без учета регистра
		else:
			list_recipe = all_recipe.filter(title__icontains = name_search, category__icontains=category_data, owner=user).order_by('-data_create')[:count_recipe] #минус перед сортировкой это чтобы перевернуть
		return render(request, 'new_recipe.html',{'data': list_recipe})
	list_recipe = all_recipe.filter(owner=user).reverse().order_by('count_view')[:settings.START_COUNT_VIEW]
	return render(request, 'list_recipe_users.html',{'data': list_recipe, 'sort_list': settings.CATEGORY_LIST, 'recipe_user': user.id, 'recipe_user_name': user.username})

@login_required
def savedListView(request):
	"""
	Обработчик сохраненных рецептов пользователя. Доступ к запросу имеют только авторизированные пользователи
	При получение POST запроса, можно указать кол-во элементов для отображения
		recipes_need(int): кол-во рецептов для выдачи
	"""
	if request.method == 'POST':
		count_recipe = int(request.POST.get('recipes_need'))
		list_recipe = SavedRecipeModel.objects.filter(saved_by = request.user).order_by('-id')[:count_recipe]
		return render(request, 'my_new_recipe.html',{'data': list_recipe})
	list_recipe = SavedRecipeModel.objects.filter(saved_by = request.user).order_by('-id')[:settings.START_COUNT_VIEW]
	return render(request, 'saved_list.html',{'data': list_recipe})

@login_required
def detail(request, id_recipe: int):
	"""
	Обработчик отельной страницы каждого рецепта. Доступ к запросу имеют только авторизированные пользователи.
	В этой функции за счет POST запроса обрабатывается и комментарии, и управление рецептом, и сохранение рецепта
	Параметры:
		id_recipe(int): ID рецепта, который нужно увидеть
	Данные POST запроса:
		type(str): тип запроса, который отправляется. Список запросов:
			update_recipe -> редактировние рецепта. Дополнительные аргументы при действие:
				title(str): новое название рецепта
				text_recipe(str): новой текст рецепта
				image(image): новое изображение рецепта
				complexity(int): новая сложность рецепта
				category(str): новая категория рецепта
			delete_recipe -> удаление рецепта
			save_recipe -> сохранение рецепта в список сохраненных у пользователя. Дополнительные аргументы при действие:
				new_text(str): измененный локального текста при сохранение рецепта
			delete_saved_recipe -> удаление рецепта из списка локальных
	"""
	recipe = RecipeModel.objects.get(id=id_recipe)
	if request.method == 'POST':
		type_fun = request.POST.get('type')
		if type_fun == 'update_recipe':
			if request.user.id != RecipeModel.objects.get(id = id_recipe).owner.id:
				return redirect("detail", id_recipe)
			recipe_title = request.POST.get('title')
			recipe_text = request.POST.get('text_recipe')
			recipe_complexity = int(request.POST.get('complexity'))
			recipe_category = request.POST.get('category')
			img = request.FILES['image']
			recipe_image = img.name
			img_byte = img.read()

			updateRecipe.delay(recipe_title,recipe_text,recipe_image,recipe_complexity,recipe_category, id_recipe, img_byte)
			return redirect("detail", id_recipe)
		elif type_fun == 'delete_recipe':
			if request.user.id != RecipeModel.objects.get(id = id_recipe).owner.id:
				return redirect("detail", id_recipe)
			RecipeModel.objects.filter(id=id_recipe).delete()
			return redirect('home')
		elif type_fun == 'save_recipe':
			new_text = request.POST.get('new_text')
			SavedRecipeModel.objects.create(
					saved_by = request.user,
					recipe = recipe,
					new_text = new_text
				)
			return redirect("detail", id_recipe)
		elif type_fun == 'delete_saved_recipe':
			SavedRecipeModel.objects.get(saved_by = request.user, recipe = recipe).delete()
		return redirect("detail", id_recipe)
	recipe.count_view += 1
	recipe.save(update_fields=["count_view"])
	form = EditRecipeForm()
	save_form = SaveRecipeForm()
	saved_user = SavedRecipeModel.objects.filter(recipe = recipe, saved_by = request.user)
	if len(saved_user) > 0:
		new_recipe_text = saved_user[0].new_text
		return render(request, 'detail_recipe.html', {'recipe': recipe, 'form':form, 'save_form':save_form, 'before_save': True, 'new_recipe_text': new_recipe_text})
	return render(request, 'detail_recipe.html', {'recipe': recipe, 'form':form, 'save_form':save_form, 'before_save': False})

@login_required
def addRecipe(request):
	"""
	Представление обработки страницы добавления нового рецепта. Доступ к запросу имеют только авторизированные пользователи.
	"""
	if request.method == 'POST':
		recipe_title = request.POST.get('title')
		recipe_text = request.POST.get('text_recipe')
		recipe_complexity = int(request.POST.get('complexity'))
		recipe_category = request.POST.get('category')
		img = request.FILES['image']
		recipe_image = img.name
		img_byte = img.read()

		newRecipe.delay(recipe_title,recipe_text,recipe_image,recipe_complexity,recipe_category, request.user.id, img_byte)
		return redirect("recipe_user", request.user.id)
	form = EditRecipeForm()
	return render(request, 'add_recipe.html', {'form': form})

@login_required
def profile(request):
	"""
	Представление профиля. Доступ к запросу имеют только авторизированные пользователи.
	"""
	if request.method == 'POST':
		field_to_update = request.POST.get('field')
		new_data = request.POST.get('data')
		if field_to_update == 'username' and len(get_user_model().objects.filter(username = new_data)) > 0: 
			return HttpResponse(False)
		if field_to_update == 'email' and (not re.fullmatch(regex, new_data) or len(get_user_model().objects.filter(email = new_data)) > 0):
			return HttpResponse(False)
		exec(f"request.user.{field_to_update} = '{new_data}'")
		request.user.save(update_fields=[field_to_update])
		cache.delete(f"{settings.USER_OBJS_NAME}:{request.user.id}")
		return HttpResponse(True)
	return render(request, 'profile.html')