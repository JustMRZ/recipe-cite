from django.urls import path
from recipe_list.views import home, detail, addRecipe, recipeByUser, profile, savedListView


urlpatterns = [
    path('', home, name='home'),
    path('recipe/<int:id_recipe>/', detail, name='detail'),
    path('add_recipe/', addRecipe, name='add'),
    path('recipe_list/<int:user_id>/', recipeByUser, name='recipe_user'),
    path('profile/', profile, name='profile'),
    path('my_recipe/',savedListView, name='my_recipe')
]
