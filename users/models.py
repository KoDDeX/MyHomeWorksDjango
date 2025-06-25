from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """Кастомная модель пользователя, наследуемая от AbstractUser"""
    first_name = None  # Убираем поле first_name
    last_name = None   # Убираем поле last_name

    # Делаем email уникальным полем и обязательным для логина
    email = models.EmailField(
        unique=True,
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default_avatar.png',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )

    USERNAME_FIELD = 'email'  # Используем email как уникальное поле для логина
    REQUIRED_FIELDS = ['username']  # username все еще нужен для AbstractUser, но можно сделать его не основным

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']
