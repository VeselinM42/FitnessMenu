from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy, reverse

from django.contrib.auth import views as auth_views, get_user_model, logout, login

from fitness_menu_app.accounts.forms import CreateUserForm, CustomPasswordChangeForm, EmailChangeForm
from fitness_menu_app.recipes.forms import CreateRecipeListForm
from fitness_menu_app.accounts.models import CustomUser
from fitness_menu_app.helpers.profiles_helper import get_profile
from fitness_menu_app.recipes.models import Recipe, RecipeLists

UserModel = get_user_model()


class SignInUserView(auth_views.LoginView):
    template_name = "accounts/signin_user.html"
    redirect_authenticated_user = True


class SignUpUserView(views.CreateView):
    template_name = "accounts/signup_user.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        result = super().form_valid(form)

        login(self.request, form.instance)

        return result


class ProfileDetailsView(views.DetailView):
    queryset = get_profile()

    template_name = "accounts/details_profile.html"


def signout_user(request):
    logout(request)
    return redirect('index')


class OwnerRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs.get('pk', None):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(views.UpdateView):
    queryset = get_profile()
    template_name = "accounts/edit_profile.html"
    fields = ("first_name", "last_name", "profile_picture")

    def get_success_url(self):
        return reverse("details profile", kwargs={
            "pk": self.object.pk,
        })

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        return form


class ProfileDeleteView(views.DeleteView):
    model = CustomUser
    template_name = "accounts/delete_profile.html"
    success_url = reverse_lazy('index')


class ProfileRecipesView(views.ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_nutrition_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()

        user_id = self.request.user.id

        queryset = queryset.filter(owner_id=user_id)

        recipe_nutrition_list = []

        for recipe in queryset:
            nutrition = recipe.nutrition.first()
            recipe_nutrition_list.append((recipe, nutrition))
        return recipe_nutrition_list


class EmailChangeView(views.UpdateView):
    queryset = get_profile()
    template_name = 'accounts/password-or-email-change.html'
    form_class = EmailChangeForm

    def get_success_url(self):
        return reverse("details profile", kwargs={
            "pk": self.object.pk,
        })

    def form_valid(self, form):
        self.request.user.email = form.cleaned_data['email']
        self.request.user.save()
        return super().form_valid(form)


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password-or-email-change.html'
    form_class = CustomPasswordChangeForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('details profile', kwargs={'pk': pk})


class CreateRecipeListView(views.CreateView):
    model = RecipeLists
    form_class = CreateRecipeListForm
    template_name = 'accounts/create_recipe_list.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('personal recipe lists', kwargs={'pk': pk})


class RecipeListsView(views.ListView):
    model = RecipeLists
    template_name = 'accounts/profile_recipe_lists.html'
    context_object_name = 'lists'

    def get_queryset(self):
        return RecipeLists.objects.filter(user=self.request.user)
