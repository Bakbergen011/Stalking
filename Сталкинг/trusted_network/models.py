"""
Модель доверенного контакта.

Хранит:
  - связь с пользователем (ForeignKey → User)
  - телефон в маскированном и хэшированном виде
  - одноразовый 6-значный SMS-код
  - флаг подтверждения
  - дату создания

Безопасность:
  - Реальный номер не хранится после маскировки
  - Код подтверждения удаляется после успешной верификации
  - Максимум 5 контактов на пользователя (проверяется во вью)
"""

import hashlib
from django.db import models
from django.conf import settings
from django.utils import timezone


class TrustedContact(models.Model):
    """Доверенное лицо пользователя."""

    STATUS_CHOICES = [
        ('pending', 'Күтуде (Ожидание)'),
        ('confirmed', 'Расталды (Подтверждён)'),
        ('muted', 'Өшірулі (Отключён)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trusted_contacts',
        verbose_name='Пользователь',
    )

    display_name = models.CharField(
        max_length=50,
        verbose_name='Имя / псевдоним',
        help_text='Отображаемое имя (лақап ат)',
    )

    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон (маскированный)',
        help_text='Маскированный номер: +7 *** ** 45',
    )

    phone_hash = models.CharField(
        max_length=64,
        verbose_name='Хэш телефона',
        help_text='SHA-256 хэш полного номера для идентификации',
        db_index=True,
    )

    sms_code = models.CharField(
        max_length=6,
        blank=True,
        default='',
        verbose_name='SMS-код подтверждения',
        help_text='6-значный одноразовый код',
    )

    code_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Срок действия кода',
    )

    confirmed = models.BooleanField(
        default=False,
        verbose_name='Подтверждён',
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус',
    )

    notifications_enabled = models.BooleanField(
        default=True,
        verbose_name='Уведомления включены',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата подтверждения',
    )

    class Meta:
        verbose_name = 'Доверенное лицо'
        verbose_name_plural = 'Доверенные лица'
        ordering = ['-created_at']
        # Один и тот же номер не может быть добавлен дважды
        unique_together = ['user', 'phone_hash']

    def __str__(self):
        return f'{self.display_name} ({self.phone}) — {self.get_status_display()}'

    @staticmethod
    def hash_phone(raw_phone: str) -> str:
        """SHA-256 хэш номера телефона."""
        clean = ''.join(c for c in raw_phone if c.isdigit())
        return hashlib.sha256(clean.encode()).hexdigest()

    @staticmethod
    def mask_phone(raw_phone: str) -> str:
        """Маскирует номер: +7 701 123 45 67 → +7 *** ** 67"""
        clean = ''.join(c for c in raw_phone if c.isdigit())
        if len(clean) < 4:
            return '***'
        return f'+7 *** ** {clean[-2:]}'

    def is_code_valid(self) -> bool:
        """Проверяет, не истёк ли срок действия кода."""
        if not self.code_expires_at:
            return False
        return timezone.now() < self.code_expires_at


class ThreatLog(models.Model):
    """Журнал активации/деактивации режима угрозы."""

    ACTION_CHOICES = [
        ('activated', 'Қосылды (Активирован)'),
        ('deactivated', 'Өшірілді (Деактивирован)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='threat_logs',
        verbose_name='Пользователь',
    )

    action = models.CharField(
        max_length=15,
        choices=ACTION_CHOICES,
        verbose_name='Действие',
    )

    contacts_notified = models.PositiveIntegerField(
        default=0,
        verbose_name='Уведомлено контактов',
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время',
    )

    class Meta:
        verbose_name = 'Запись журнала угроз'
        verbose_name_plural = 'Журнал угроз'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user} — {self.get_action_display()} ({self.timestamp:%d.%m.%Y %H:%M})'
