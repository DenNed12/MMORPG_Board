from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from django import forms
import random
from django.conf import settings
from django.core.mail import send_mail
class RegisterForm(UserCreationForm):
    # first_name = forms.CharField(label = "Имя") # опционально
    # last_name = forms.CharField(label = "Фамилия") # опционально
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Confirm Password')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # 'password1': forms.PasswordInput(attrs={'class': 'form-control'}), # Для паролей виджет не работает. Чтобы задать атрибуты, например, название класса, следует использовать поле модели.
            # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return super().clean()

    def save(self,commit=True):
        user = super().save(commit=True)
        user.is_active = False
        code = random.randint(1111, 9999)
        user.code = code
        user.save()
        send_mail(
            subject="Код подтверждения пользователя",
            message=f'{user.code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            "username",
            # "email",
            "password",
        )


class CodeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('code',)