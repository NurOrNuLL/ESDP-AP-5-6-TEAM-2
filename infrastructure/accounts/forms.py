from django import forms
from .models import CustomUser
from .validators import (
    number_validate, uppercase_validate, symbol_validate,
    len_validate, cyrillic_validate, len_username_validate,
    cyrillic_username_validate
)


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин', required=True, validators=(len_username_validate, cyrillic_username_validate, )
    )
    password = forms.CharField(
        label="Пароль", strip=False, required=True, widget=forms.PasswordInput,
        validators=(
            number_validate, uppercase_validate, symbol_validate,
            len_validate, cyrillic_validate,
        )
    )
    password_confirm = forms.CharField(
        label="Подтвердите пароль", required=True, widget=forms.PasswordInput, strip=False
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.errors['password'] = 'Пароли не совпадают!'
            self.errors['password_confirm'] = 'Пароли не совпадают!'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm']
