"""
Регистрация моделей в Django Admin.
"""

from django.contrib import admin
from .models import TrustedContact, ThreatLog


@admin.register(TrustedContact)
class TrustedContactAdmin(admin.ModelAdmin):
    list_display = [
        'display_name', 'phone', 'status', 'confirmed',
        'notifications_enabled', 'user', 'created_at',
    ]
    list_filter = ['status', 'confirmed', 'notifications_enabled']
    search_fields = ['display_name', 'phone']
    readonly_fields = ['phone_hash', 'created_at', 'confirmed_at']
    list_per_page = 25


@admin.register(ThreatLog)
class ThreatLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'contacts_notified', 'timestamp']
    list_filter = ['action']
    readonly_fields = ['timestamp']
    list_per_page = 50
