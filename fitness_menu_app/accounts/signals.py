from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from fitness_menu_app.accounts.models import CustomUser

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):

    if not created:
        return

    CustomUser.objects.create(user=instance, pk=instance.id)


@receiver(post_delete, sender=CustomUser)
def post_delete_profile(sender, instance, *args, **kwargs):
    instance.recipes.all().delete()
