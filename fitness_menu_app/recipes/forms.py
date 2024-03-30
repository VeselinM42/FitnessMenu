from django import forms

# from fitness_menu_app.accounts.models import RecipeLists
from fitness_menu_app.recipes.models import Recipe, Review, RecipeLists, Nutrition


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'type', 'description', 'image_url']


class NutritionForm(forms.ModelForm):
    class Meta:
        model = Nutrition
        fields = ['calories', 'protein', 'carbs', 'fats']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class CreateRecipeListForm(forms.ModelForm):
    class Meta:
        model = RecipeLists
        fields = ['name']
