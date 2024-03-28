from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views

# from fitness_menu_app.accounts.models import RecipeLists
# from fitness_menu_app.recipes.forms import AddRecipeToListForm
from fitness_menu_app.recipes.models import Recipe, Review, RecipeLists


class CreateRecipeView(LoginRequiredMixin, views.CreateView):
    model = Recipe
    fields = ("name", "type", "description", "image_url", "calories", "protein", "carbs", "fats")
    template_name = "recipes/add_recipe.html"
    success_url = reverse_lazy("recipes list")

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


class DetailsRecipeView(views.DetailView):
    model = Recipe
    template_name = 'recipes/recipe-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        average_rating = recipe.review_set.aggregate(Avg('rating'))['rating__avg']
        context['has_rated'] = Review.objects.filter(recipe=recipe, user=self.request.user).exists()
        context['average_rating'] = average_rating
        context['lists'] = RecipeLists.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs['pk']
        list_id = request.POST.get('list_id')
        if list_id:
            recipe = Recipe.objects.get(pk=recipe_id)
            recipe_list = RecipeLists.objects.get(pk=list_id)
            recipe_list.recipes.add(recipe)
        return redirect('details recipe', pk=recipe_id)


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


class ReviewCreateView(views.CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'recipes/recipe-review.html'
    success_url = reverse_lazy('details recipe')

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])

    def test_func(self):
        recipe = self.get_recipe()
        return super().test_func() and not Review.objects.filter(recipe=recipe, user=self.request.user).exists()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.recipe = self.get_recipe()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("details recipe", kwargs={
            "pk": self.kwargs['pk'],
        })


def add_to_list(request, pk):
    if request.method == 'POST':
        list_id = request.POST.get('list_id')
        if list_id:
            recipe = get_object_or_404(Recipe, pk=pk)
            recipe_list = get_object_or_404(RecipeLists, pk=list_id)
            recipe_list.recipes.add(recipe)
            return redirect('details recipe', pk=pk)


class PersonalRecipeListView(views.ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'page_obj'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_id = self.kwargs['list_id']
        recipe_list = get_object_or_404(RecipeLists, pk=list_id)
        paginator = Paginator(recipe_list.recipes.all(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
