from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Order (models.Model):
    """
    Модель для хранения информации о заказах клиентов.
    Использует связи с моделями Master и Service для связи с мастерами и услугами.
    С моделью Master связь многие-к-одному.
    С моделью Service связь многие-ко-многим через поле orders.
    """
    STATUS_CHOICES = [
    ("not_approved", "Не подтверждено"),
    ("approved", "Подтверждено"),
    ("completed", "Выполнено"),
    ("cancelled", "Отменено"),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Мастер")
    services = models.ManyToManyField("Service", related_name="orders", verbose_name="Услуги")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    def __str__(self):
        return f"Заказ {self.id} от {self.client_name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date_created"]

        # Индексы для ускорения поиска
        indexes = [
            models.Index(fields=["client_name"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["comment"]),
            models.Index(fields=["client_name", "phone", "comment"], name="name_phone_comment_index"),
        ]

class Master (models.Model):
    """
    Модель для хранения информации о мастерах барбершопа.
    Использует связи с моделью Service для связи с услугами.
    С моделью Service связь многие-ко-многим через поле masters.
    """
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", related_name="masters", verbose_name="Услуги")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    view_count = models.PositiveIntegerField(
    default=0, verbose_name="Количество просмотров"
    )   

    def avg_rating(self)-> float:
        """Вычисляет среднюю оценку мастера на основе опубликованных отзывов"""
    # Получаем только опубликованные отзывы
        published_reviews = self.reviews.filter(is_published=True)
        
        # Проверяем, есть ли отзывы
        if published_reviews.exists():
            # Вычисляем среднее значение и округляем до 1 знака после запятой
            return round(sum(review.rating for review in published_reviews) / published_reviews.count(), 1)
        else:
            # Если отзывов нет, возвращаем 0 или None
            return 0.0

    def __str__(self):
        return f"{self.name}"


class Service (models.Model):
    """
    Модель для хранения информации об услугах барбершопа.
    Использует связи с моделью Master для связи с мастерами.
    С моделью Master связь многие-ко-многим через поле services.
    """
    name = models.CharField (max_length=200, verbose_name="Название")
    description = models.TextField (verbose_name="Описание")
    price = models.DecimalField (max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField (verbose_name="Длительность", help_text="Время выполнения в минутах", default=30)
    is_popular = models.BooleanField (verbose_name="Популярная услуга", default=False)
    image = models.ImageField (upload_to="services/", verbose_name="Изображение", blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class Review (models.Model):
    """
    Модель для хранения информации об отзывах клиентов.
    Использует связи с моделью Master для связи с мастерами.
    С моделью Master связь многие-к-одному.
    """
    text= models.TextField (verbose_name="Текст отзыва")
    client_name= models.CharField (max_length=100, blank=True, verbose_name="Имя клиента")
    master= models.ForeignKey ("Master", on_delete=models.CASCADE, related_name="reviews", verbose_name="Мастер")
    photo= models.ImageField (upload_to="images/reviews/", blank=True, null=True, verbose_name="Фотография")
    created_at= models.DateTimeField (auto_now_add=True, verbose_name="Дата создания")
    rating= models.PositiveSmallIntegerField (validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оценка")
    is_published= models.BooleanField (default=False, verbose_name="Опубликован")

    def __str__(self):
        return f"Отзыв {self.id} [{self.client_name} от {self.created_at.strftime('%d/%m/%Y')}]"