from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class CreateUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('username', 'email')
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }


class FitnessMenuChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
