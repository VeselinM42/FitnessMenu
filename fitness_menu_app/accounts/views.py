from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import generic as views
from django.urls import reverse_lazy, reverse

from django.contrib.auth import views as auth_views, get_user_model, logout, login

from fitness_menu_app.accounts.forms import CreateUserForm
from fitness_menu_app.accounts.models import CustomUser
from fitness_menu_app.helpers.profiles_helper import get_profile
from fitness_menu_app.recipes.models import Recipe

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
    """Verify that the current user has this profile."""

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


@login_required
def profile_recipes_list(request, pk):
    user_id = pk
    profile_recipes = Recipe.objects.filter(owner_id=user_id)

    paginator = Paginator(profile_recipes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'recipes/recipe_list.html', context)
