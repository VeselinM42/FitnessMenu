from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

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


class ChangeUserFrom(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email']


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
