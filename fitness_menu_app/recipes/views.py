from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from fitness_menu_app.recipes.models import Recipe


class CreateRecipeView(LoginRequiredMixin, views.CreateView):
    model = Recipe
    fields = ("name", "type", "description", "image_url", "calories", "protein", "carbs", "fats")
    template_name = "recipes/add_recipe.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


class DetailsRecipeView(views.DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipes/recipe-details.html'


class UpdateRecipeView(views.UpdateView):
    model = Recipe
    fields = ("description", "image_url", "calories", "protein", "carbs", "fats")
    template_name = "recipes/edit-recipe.html"

    def get_success_url(self):
        return reverse("details recipe", kwargs={
            "pk": self.object.pk,
        })


class RecipeDeleteView(views.DeleteView):
    model = Recipe
    template_name = "recipes/delete-recipe.html"
    success_url = reverse_lazy('recipes list')


def recipes_list(request):
    all_recipes = Recipe.objects.order_by('-created_at')

    paginator = Paginator(all_recipes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, "recipes/recipe_list.html", context)
