from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from fitness_menu_app.recipes.forms import NutritionForm, RecipeForm
# from fitness_menu_app.accounts.models import RecipeLists
# from fitness_menu_app.recipes.forms import AddRecipeToListForm
from fitness_menu_app.recipes.models import Recipe, Review, RecipeLists, Nutrition


class CreateRecipeView(LoginRequiredMixin, views.CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/add_recipe.html"
    success_url = reverse_lazy("recipes list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['nutrition_form'] = NutritionForm(self.request.POST)
        else:
            context['nutrition_form'] = NutritionForm()
        return context

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        context = self.get_context_data()
        nutrition_form = context['nutrition_form']
        if form.is_valid() and nutrition_form.is_valid():
            self.object = form.save()
            nutrition_info = nutrition_form.save(commit=False)
            nutrition_info.recipe = self.object
            nutrition_info.save()
            return super().form_valid(form)
        else:
            # Handle form validation errors
            return self.form_invalid(form)


class DetailsRecipeView(views.DetailView):
    model = Recipe
    template_name = 'recipes/recipe-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        average_rating = recipe.review_set.aggregate(Avg('rating'))['rating__avg']
        nutrition = get_object_or_404(Nutrition, recipe=recipe)
        context['has_rated'] = Review.objects.filter(recipe=recipe, user=self.request.user).exists()
        context['average_rating'] = average_rating
        context['lists'] = RecipeLists.objects.filter(user=self.request.user)
        context['nutrition'] = nutrition
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
    form_class = RecipeForm
    template_name = "recipes/edit-recipe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = RecipeForm(self.request.POST, instance=self.object)
            context['nutrition_form'] = NutritionForm(self.request.POST)
        else:
            context['form'] = RecipeForm(instance=self.object)
            nutrition_instance = self.object.nutrition.first()
            context['nutrition_form'] = NutritionForm(instance=nutrition_instance)
        return context

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        context = self.get_context_data()
        nutrition_form = context['nutrition_form']
        if form.is_valid() and nutrition_form.is_valid():
            self.object = form.save()
            nutrition_info = nutrition_form.save(commit=False)
            nutrition_info.recipe = self.object
            nutrition_info.save()
            return super().form_valid(form)
        else:
            # Handle form validation errors
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("details recipe", kwargs={"pk": self.object.pk})


class RecipeDeleteView(views.DeleteView):
    model = Recipe
    template_name = "recipes/delete-recipe.html"
    success_url = reverse_lazy('recipes list')



class RecipeListView(views.ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipe_nutrition_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()

        recipe_nutrition_list = []

        for recipe in queryset:
            nutrition = recipe.nutrition.first()
            recipe_nutrition_list.append((recipe, nutrition))
        return recipe_nutrition_list


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
    context_object_name = 'recipe_nutrition_list'
    paginate_by = 3

    def get_queryset(self):
        list_id = self.kwargs['list_id']
        recipe_list = get_object_or_404(RecipeLists, pk=list_id)
        queryset = recipe_list.recipes.all()

        recipe_nutrition_list = []

        for recipe in queryset:
            nutrition = recipe.nutrition.first()
            recipe_nutrition_list.append((recipe, nutrition))
        return recipe_nutrition_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_id = self.kwargs['list_id']
        recipe_list = get_object_or_404(RecipeLists, pk=list_id)
        paginator = Paginator(recipe_list.recipes.all(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
