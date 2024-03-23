from fitness_menu_app.accounts.models import CustomUser


def get_profile():
    return CustomUser.objects.all()
