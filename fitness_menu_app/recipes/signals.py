from django.db.models.signals import post_delete
from django.dispatch import receiver

from fitness_menu_app.recipes.models import Recipe


@receiver(post_delete, sender=Recipe)
def post_delete_recipe(sender, instance, *args, **kwargs):
    instance.nutrition.all().delete()
