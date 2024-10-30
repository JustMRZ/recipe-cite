from django.urls import path
from api.views import updateComment, newLike, deleteComment, newComment


urlpatterns = [
	path('update_comment', updateComment, name='update_comment'),
	path('new_like', newLike, name='new_like'),
	path('delete_comment', deleteComment, name='delete_comment'),
	path('add_comment', newComment, name='add_comment'),
]