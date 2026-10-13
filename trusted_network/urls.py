"""
URL-маршруты модуля «Сеть доверенных лиц».

Подключение в корневом urls.py:
    path('trusted/', include('trusted_network.urls')),
"""

from django.urls import path
from . import views

app_name = 'trusted_network'

urlpatterns = [
    # Главная страница
    path('', views.trusted_network_page, name='page'),

    # Добавление контакта
    path('add/', views.add_trusted_contact, name='add'),

    # Подтверждение кода
    path('verify/<int:contact_id>/', views.verify_contact, name='verify'),

    # Удаление контакта
    path('delete/<int:contact_id>/', views.delete_contact, name='delete'),

    # Переключение mute/unmute
    path('toggle-mute/<int:contact_id>/', views.toggle_mute, name='toggle_mute'),

    # Режим угрозы
    path('threat-on/', views.threat_on, name='threat_on'),
    path('threat-off/', views.threat_off, name='threat_off'),

    # Удалить все
    path('delete-all/', views.delete_all_contacts, name='delete_all'),
]
