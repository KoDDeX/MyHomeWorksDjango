from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    """
    Кастомная форма для входа пользователей
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Имя пользователя или email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

        # Убираем helptext для полей формы
        for field_name in ('username', 'password'):
            if self.fields.get(field_name):
                self.fields[field_name].help_text = None

class UserRegisterForm(UserCreationForm):
    """
    Кастомная форма для регистрации пользователей
    """
    # Добавляем поле email тип EmailField
    email = forms.EmailField(
        label="Email",
        max_length=254,
        help_text="Введите ваш email",
        widget=forms.EmailInput(attrs={"class": "form-control mb-2", "placeholder": "Введите ваш email"}),
        required=True,
    )
    
    class Meta:
        model = get_user_model()
        # Включаем username и email в форму регистрации
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Имя пользователя'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Придумайте пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })

        # Убираем helptext для полей формы
        for field_name in ('username', 'password1', 'password2', 'email'):
            if self.fields.get(field_name):
                self.fields[field_name].help_text = None


    def save(self, commit=True):
        """"
        Переопределяем метод save для корректного сохранения поля email
        """
        user = super().save(commit=True)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        """
        Проверяем уникальность email
        """
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email