from django.contrib import admin
from recipe_list.models import RecipeModel, CommentModel, LikesCommentModel, SavedRecipeModel

# Register your models here.
admin.site.register(RecipeModel)
admin.site.register(CommentModel)
admin.site.register(LikesCommentModel)
admin.site.register(SavedRecipeModel)