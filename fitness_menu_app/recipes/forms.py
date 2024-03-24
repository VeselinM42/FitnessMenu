from django import forms

from fitness_menu_app.recipes.models import Recipe, Review


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'type', 'description', 'image_url', 'calories', 'protein', 'carbs', 'fats']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']