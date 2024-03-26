from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from fitness_menu_app.accounts.models import CustomUser

UserModel = get_user_model()


class RecipeTypes(models.TextChoices):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"
    DESSERT = "Dessert"


class Recipe(models.Model):
    RECIPE_NAME_MAX_LENGTH = 50
    RECIPE_TYPE_MAX_LENGTH = 30

    name = models.CharField(
        max_length=RECIPE_NAME_MAX_LENGTH,
        unique=False,
        blank=False,
        null=False,
    )

    type = models.CharField(
        max_length=RECIPE_TYPE_MAX_LENGTH,
        choices=RecipeTypes.choices,
        null=False,
        blank=False,
    )

    description = models.TextField(
        blank=False,
        null=False,
    )

    image_url = models.URLField(
        blank=True,
        null=True,
    )

    calories = models.IntegerField(
        blank=False,
        null=False,
    )

    protein = models.FloatField(
        blank=False,
        null=False,
    )

    carbs = models.FloatField(
        blank=False,
        null=False,
    )

    fats = models.FloatField(
        blank=False,
        null=False,
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='recipes',
    )

    created_at = models.DateTimeField(
        _("created_at"),
        default=timezone.now,
    )

    def save(self, *args, **kwargs):
        if not self.owner_id and 'request' in kwargs:
            self.owner = kwargs['request'].user
        super().save(*args, **kwargs)


class Review(models.Model):
    MAX_RATE_VALUE = 5

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
        default=0,
    )

    comment = models.TextField(
        blank=True,
        null=True,
    )


class RecipeLists(models.Model):

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100
    )

    recipes = models.ManyToManyField(
        Recipe,
        related_name='lists',
        blank=True
    )
