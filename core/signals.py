# Опишем сигнал, который будет слушать создание записи в модель Review и проверять есть ли в поле text слова "плохо" или "ужасно". - Если нет, то меняем is_published на True

from .models import Order
from django.db.models.signals import post_save
from django.dispatch import receiver
# Импорт всего что нужно для работы бота
from .telegram_bot import send_telegram_message
from asyncio import run
# Из настроек импортируем токен и id чата
from django.conf import settings

TELEGRAM_BOT_API_KEY = settings.TELEGRAM_BOT_API_KEY
TELEGRAM_USER_ID = settings.TELEGRAM_USER_ID


@receiver(post_save, sender=Order)
def telegram_order_notification(sender, instance, created, **kwargs):
    pass

