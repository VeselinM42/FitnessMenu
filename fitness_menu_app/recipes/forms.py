from django import forms

# from fitness_menu_app.accounts.models import RecipeLists
from fitness_menu_app.recipes.models import Recipe, Review, RecipeLists


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'type', 'description', 'image_url', 'calories', 'protein', 'carbs', 'fats']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


# class AddRecipeToListForm(forms.ModelForm):
#     class Meta:
#         model = RecipeLists
#         fields = ['name']


class CreateRecipeListForm(forms.ModelForm):
    class Meta:
        model = RecipeLists
        fields = ['name']
