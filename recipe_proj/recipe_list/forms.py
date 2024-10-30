from django import forms 
from recipe_list.models import RecipeModel, SavedRecipeModel
from tinymce.widgets import TinyMCE
from recipe_proj.settings import CATEGORY_LIST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class EditRecipeForm(forms.ModelForm):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': ' '}))
	category = forms.ChoiceField(choices=CATEGORY_LIST)
	text_recipe = forms.CharField(
				widget=TinyMCEWidget(
				attrs={'required': False, 'cols': 10, 'rows': 10}
			)
		)
	image = forms.ImageField()
	complexity = forms.IntegerField(min_value=1, max_value=10, widget=forms.NumberInput(attrs={'min': 1, 'max': 10, 'placeholder': ' '}))
	
	class Meta:
		model = RecipeModel
		fields = ['title','text_recipe','image','complexity','category']

class SaveRecipeForm(forms.ModelForm):
	new_text = forms.CharField(
				widget=TinyMCEWidget(
				attrs={'required': False, 'cols': 10, 'rows': 10}
			)
		)
	class Meta:
		model = SavedRecipeModel
		fields = ['new_text', ]
