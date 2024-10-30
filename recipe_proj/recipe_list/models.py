from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from tinymce.models import HTMLField
from django.urls import reverse
from django.core.cache import cache
from django.conf import settings

#from recipe_proj.settings import TINYMCE_PROFILE

# Create your models here.
class RecipeModel(models.Model):
	"""
	Модель хранения рецептов:
	Атрибуты:
		title(CharField): название рецепта
		text_recipe(HTMLField): текст рецепта
		image_url(CharField): изображение рецепта
		complexity(IntegerField): сложность рецепта
		owner(User): объект владельца рецепта
		data_create(DateTimeField): время создание рецепта
		count_view(PositiveIntegerField): кол-во просмотров рецепту
	Методы:
		get_absolute_url: получение ссылки на отдельную страницу рецепта
	"""
	title = models.CharField(max_length=100)
	text_recipe = HTMLField()
	#image = models.ImageField()
	image_url = models.CharField(blank=True)
	complexity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	category = models.CharField(max_length=50)
	owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE )
	data_create = models.DateTimeField(auto_now_add=True)
	count_view = models.PositiveIntegerField(default=0)

	def __str__(self):
		return f"{self.id}. {self.title if len(self.title) < 20 else self.title[:20] + '...'} (by {self.owner})"

	def get_absolute_url(self):
		return reverse('detail', args=[self.id])

	def save(self, *args, **kwargs):
		cache.delete(f"{settings.RECIPE_LIST_NAME}")
		return super().save(*args, **kwargs)


class CommentModel(models.Model):
	"""
	Модель хранения комментариев:
	Атрибуты:
		owner(User): объект владельца комментария
		recipe(RecipeModel): рецепт, к которому комментарий
		data_create(DateTimeField): время создание комментария
		comment(TextField): текст комментария
	"""
	owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	recipe = models.ForeignKey(RecipeModel , on_delete=models.CASCADE)
	data_create = models.DateTimeField(auto_now_add=True)
	comment = models.TextField()

	def __str__(self):
		return f"{self.id}. Комментарий статьи {self.recipe.title}. {self.comment if len(self.comment) < 20 else self.comment[:20] + '...'} (by {self.owner})"

	def save(self, *args, **kwargs):
		cache.delete(f'{settings.COMMENTS_LIST_NAME}:{self.recipe.id}')
		return super().save(*args, **kwargs)

class LikesCommentModel(models.Model):
	"""
	Модель хранения лайков
	Атрибуты:
		owner(User): объект владельца лайка
		comment(CommentModel): комментарий, к которому относится лайк
		data_added(DateTimeField): время создание лайка
	"""
	owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE)
	data_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.id}. Нравиться от {self.owner} на комментарий к статье {self.comment.recipe.title}"

class SavedRecipeModel(models.Model):
	"""
	Модель хранения сохраненных рецептов пользователями
	Атрибуты:
		recipe(User): объект владельца рецепта
		recipe(RecipeModel): рецепт, к которомый сохраняется
		new_text(HTMLField): Новый текст рецепта
	"""
	saved_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	recipe = models.ForeignKey(RecipeModel , on_delete=models.CASCADE)
	new_text = HTMLField()
	def __str__(self):
		return f"{self.id}. Сохранено от {self.saved_by} для {self.recipe}"