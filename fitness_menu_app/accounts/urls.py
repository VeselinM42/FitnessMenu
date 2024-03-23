from django.urls import path, include
from fitness_menu_app.accounts.views import SignInUserView, SignUpUserView, ProfileDetailsView, signout_user, \
    ProfileUpdateView, ProfileDeleteView, profile_recipes_list

urlpatterns = (
    path("signup/", SignUpUserView.as_view(), name="signup user"),
    path("signin/", SignInUserView.as_view(), name="signin user"),
    path("signout/", signout_user, name="signout user"),

    path("profile/<int:pk>/", include([
        path('', ProfileDetailsView.as_view(), name="details profile"),
        path("edit/", ProfileUpdateView.as_view(), name="edit profile"),
        path("delete/", ProfileDeleteView.as_view(), name="delete profile"),
        path("recipes/", profile_recipes_list, name="profile recipes")
    ]))
)
