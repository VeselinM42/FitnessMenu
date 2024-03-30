from django.urls import path, include

from fitness_menu_app.recipes.views import CreateRecipeView, RecipeListView, DetailsRecipeView, UpdateRecipeView, \
    RecipeDeleteView, ReviewCreateView, add_to_list, PersonalRecipeListView

urlpatterns = (
    path('add-recipe/', CreateRecipeView.as_view(), name='add recipe'),
    path('list/', RecipeListView.as_view(), name='recipes list'),
    path('recipe/<int:pk>/', include([
        path('', DetailsRecipeView.as_view(), name='details recipe'),
        path('edit/', UpdateRecipeView.as_view(), name='edit-recipe'),
        path('delete/', RecipeDeleteView.as_view(), name='delete-recipe'),
        path('review/', ReviewCreateView.as_view(), name='recipe-review'),
        path('add-to-list/', add_to_list, name='add-to-list'),
    ])),
    path('personal-list/<int:list_id>/', PersonalRecipeListView.as_view(), name="personal recipe list"),
)
