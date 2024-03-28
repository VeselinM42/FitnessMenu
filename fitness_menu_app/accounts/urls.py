from django.urls import path, include
from fitness_menu_app.accounts.views import SignInUserView, SignUpUserView, ProfileDetailsView, signout_user, \
    ProfileUpdateView, ProfileDeleteView, profile_recipes_list, EmailChangeView, PasswordChangeView, RecipeListsView, \
    CreateRecipeListView
from fitness_menu_app.recipes.views import PersonalRecipeListView

urlpatterns = (
    path("signup/", SignUpUserView.as_view(), name="signup user"),
    path("signin/", SignInUserView.as_view(), name="signin user"),
    path("signout/", signout_user, name="signout user"),

    path("profile/<int:pk>/", include([
        path('', ProfileDetailsView.as_view(), name="details profile"),
        path("edit/", ProfileUpdateView.as_view(), name="edit profile"),
        path("delete/", ProfileDeleteView.as_view(), name="delete profile"),
        path("recipes/", profile_recipes_list, name="profile recipes"),
        path('password-change/', PasswordChangeView.as_view(), name='password change'),
        path('email-change/', EmailChangeView.as_view(), name='email change'),
        path('personal-recipe-lists/', include([
            path('', RecipeListsView.as_view(), name="personal recipe lists"),
            path('create-recipe-list/', CreateRecipeListView.as_view(), name="create recipe list"),
        ])),
    ]))
)
