from django.urls import path, include

from fitness_menu_app.recipes.views import CreateRecipeView, recipes_list, DetailsRecipeView, UpdateRecipeView, \
    RecipeDeleteView, ReviewCreateView

urlpatterns = (
    path('add-recipe/', CreateRecipeView.as_view(), name='add recipe'),
    path('list/', recipes_list, name='recipes list'),
    path('recipe/<int:pk>/', include([
        path('', DetailsRecipeView.as_view(), name='details recipe'),
        path('edit/', UpdateRecipeView.as_view(), name='edit-recipe'),
        path('delete/', RecipeDeleteView.as_view(), name='delete-recipe'),
        path('review/', ReviewCreateView.as_view(), name='recipe-review'),
    ])),
)
