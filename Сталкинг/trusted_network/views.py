"""
Вью модуля «Сеть доверенных лиц».

Эндпоинты:
  - /trusted/                   → страница управления (GET)
  - /trusted/add/               → добавление контакта (POST → JSON)
  - /trusted/verify/<id>/       → подтверждение кода (POST → JSON)
  - /trusted/delete/<id>/       → удаление контакта (POST → JSON)
  - /trusted/toggle-mute/<id>/  → вкл/выкл уведомлений (POST → JSON)
  - /trusted/threat-on/         → активация режима угрозы (POST → JSON)
  - /trusted/threat-off/        → деактивация режима угрозы (POST → JSON)
  - /trusted/delete-all/        → удаление всех контактов (POST → JSON)
"""

import random
from datetime import timedelta

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone

from .models import TrustedContact, ThreatLog


MAX_CONTACTS = 5
CODE_EXPIRY_HOURS = 24


def _feature_unavailable():
    return JsonResponse({
        'status': 'unavailable',
        'message': 'Бұл функция қауіпсіз SMS/хабарлама жіберу қызметі қосылғанша уақытша қолжетімсіз. / Эта функция отключена до подключения безопасного сервиса доставки.',
    }, status=503)


def _generate_code() -> str:
    """Генерирует 6-значный числовой код."""
    return str(random.randint(100000, 999999))


# ─────────────────────────────────────────────
# Главная страница модуля
# ─────────────────────────────────────────────
@login_required
@require_GET
def trusted_network_page(request):
    """
    GET /trusted/
    Рендерит HTML-страницу со списком контактов.
    """
    return render(request, 'trusted_network/unavailable.html')


# ─────────────────────────────────────────────
# Добавление контакта
# ─────────────────────────────────────────────
@login_required
@require_POST
def add_trusted_contact(request):
    """
    POST /trusted/add/
    Тело: { name, phone }

    Логика:
      1. Валидация имени и телефона
      2. Проверка лимита (max 5)
      3. Проверка дубликата по хэшу
      4. Генерация 6-значного кода
      5. Сохранение записи
      6. Возврат JSON с demo_code
    """
    return _feature_unavailable()
    name = request.POST.get('name', '').strip()
    raw_phone = request.POST.get('phone', '').strip()

    # --- Валидация ---
    if not name:
        return JsonResponse({
            'status': 'error',
            'message': 'Атын енгізіңіз (Введите имя)',
        }, status=400)

    clean_phone = ''.join(c for c in raw_phone if c.isdigit())
    if len(clean_phone) < 10:
        return JsonResponse({
            'status': 'error',
            'message': 'Телефон нөмірін дұрыс енгізіңіз (Введите корректный номер)',
        }, status=400)

    # --- Проверка лимита ---
    current_count = TrustedContact.objects.filter(user=request.user).count()
    if current_count >= MAX_CONTACTS:
        return JsonResponse({
            'status': 'error',
            'message': f'Максимум {MAX_CONTACTS} адам қосуға болады (Лимит {MAX_CONTACTS})',
        }, status=400)

    # --- Проверка дубликата ---
    phone_hash = TrustedContact.hash_phone(raw_phone)
    if TrustedContact.objects.filter(user=request.user, phone_hash=phone_hash).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Бұл нөмір бұрыннан қосылған (Этот номер уже добавлен)',
        }, status=400)

    # --- Генерация кода и сохранение ---
    code = _generate_code()
    masked = TrustedContact.mask_phone(raw_phone)

    contact = TrustedContact.objects.create(
        user=request.user,
        display_name=name,
        phone=masked,
        phone_hash=phone_hash,
        sms_code=code,
        code_expires_at=timezone.now() + timedelta(hours=CODE_EXPIRY_HOURS),
        status='pending',
        confirmed=False,
    )

    # ────────────────────────────────────────
    # В ПРОДАКШЕНЕ здесь была бы отправка SMS:
    #   sms_gateway.send(to=raw_phone, text=f'ҚОРҒАУ: Растау коды: {code}')
    # Для демо — код возвращается в JSON.
    # ────────────────────────────────────────

    return JsonResponse({
        'status': 'ok',
        'contact_id': contact.id,
        'name': contact.display_name,
        'phone': contact.phone,
        'demo_code': code,          # Только для демо! В продакшене убрать.
        'message': f'✅ {name} сәтті қосылды!',
    })


# ─────────────────────────────────────────────
# Подтверждение кода
# ─────────────────────────────────────────────
@login_required
@require_POST
def verify_contact(request, contact_id):
    """
    POST /trusted/verify/<id>/
    Тело: { code }

    Принимает 6-значный код и подтверждает контакт.
    """
    return _feature_unavailable()
    try:
        contact = TrustedContact.objects.get(
            id=contact_id,
            user=request.user,
        )
    except TrustedContact.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Контакт табылмады (Контакт не найден)',
        }, status=404)

    code = request.POST.get('code', '').strip()

    if len(code) != 6:
        return JsonResponse({
            'status': 'error',
            'message': '6 санды толық енгізіңіз (Введите 6 цифр)',
        }, status=400)

    # Проверка срока действия
    if not contact.is_code_valid():
        return JsonResponse({
            'status': 'error',
            'message': 'Код мерзімі өтті (Код истёк). Жаңа код сұраңыз.',
        }, status=400)

    # Проверка кода
    if code != contact.sms_code:
        return JsonResponse({
            'status': 'error',
            'message': '❌ Код қате! Қайта көріңіз. (Неверный код)',
        }, status=400)

    # Подтверждение
    contact.confirmed = True
    contact.status = 'confirmed'
    contact.confirmed_at = timezone.now()
    contact.sms_code = ''   # Удаляем код после использования
    contact.code_expires_at = None
    contact.save()

    return JsonResponse({
        'status': 'ok',
        'message': f'✅ {contact.display_name} сәтті расталды!',
    })


# ─────────────────────────────────────────────
# Удаление контакта
# ─────────────────────────────────────────────
@login_required
@require_POST
def delete_contact(request, contact_id):
    """
    POST /trusted/delete/<id>/
    Удаляет одного доверенного.
    """
    deleted, _ = TrustedContact.objects.filter(
        id=contact_id,
        user=request.user,
    ).delete()

    if deleted:
        return JsonResponse({'status': 'ok', 'message': 'Контакт жойылды'})
    return JsonResponse({'status': 'error', 'message': 'Табылмады'}, status=404)


# ─────────────────────────────────────────────
# Переключение mute/unmute
# ─────────────────────────────────────────────
@login_required
@require_POST
def toggle_mute(request, contact_id):
    """
    POST /trusted/toggle-mute/<id>/
    Вкл/выкл уведомления для контакта.
    """
    return _feature_unavailable()
    try:
        contact = TrustedContact.objects.get(id=contact_id, user=request.user)
    except TrustedContact.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Табылмады'}, status=404)

    if contact.status == 'muted':
        contact.status = 'confirmed'
        contact.notifications_enabled = True
        msg = f'{contact.display_name} — хабарламалар қосылды 🔔'
    else:
        contact.status = 'muted'
        contact.notifications_enabled = False
        msg = f'{contact.display_name} — хабарламалар өшірілді 🔕'

    contact.save()
    return JsonResponse({'status': 'ok', 'message': msg})


# ─────────────────────────────────────────────
# Режим угрозы — активация
# ─────────────────────────────────────────────
@login_required
@require_POST
def threat_on(request):
    """
    POST /trusted/threat-on/
    Активирует режим угрозы.

    В продакшене здесь отправляются SMS/Email всем confirmed контактам:
      «ҚОРҒАУ: [Псевдоним] қауіп режимін қосты.
       Бәрі жақсы екенін тексеріңізші.»
    """
    return _feature_unavailable()
    confirmed = TrustedContact.objects.filter(
        user=request.user,
        status='confirmed',
    )
    count = confirmed.count()

    if count == 0:
        return JsonResponse({
            'status': 'error',
            'message': '⚠ Кемінде 1 расталған сенімді адам қажет!',
        }, status=400)

    # ── В продакшене: отправка SMS каждому ──
    # for contact in confirmed:
    #     real_phone = decrypt(contact.phone_hash)
    #     sms_gateway.send(
    #         to=real_phone,
    #         text=f'ҚОРҒАУ: {request.user.get_short_name()} қауіп режимін қосты. '
    #              'Бәрі жақсы екенін тексеріңізші.'
    #     )

    # Логирование
    ThreatLog.objects.create(
        user=request.user,
        action='activated',
        contacts_notified=count,
    )

    return JsonResponse({
        'status': 'ok',
        'notified': count,
        'message': f'🚨 Қауіп режимі қосылды! {count} адамға хабарлама жіберілді.',
    })


# ─────────────────────────────────────────────
# Режим угрозы — деактивация
# ─────────────────────────────────────────────
@login_required
@require_POST
def threat_off(request):
    """
    POST /trusted/threat-off/
    Деактивирует режим угрозы.
    """
    return _feature_unavailable()
    confirmed_count = TrustedContact.objects.filter(
        user=request.user,
        status='confirmed',
    ).count()

    ThreatLog.objects.create(
        user=request.user,
        action='deactivated',
        contacts_notified=confirmed_count,
    )

    return JsonResponse({
        'status': 'ok',
        'message': '✅ Қауіп режимі өшірілді. Жағдай қалыпты.',
    })


# ─────────────────────────────────────────────
# Удалить все контакты
# ─────────────────────────────────────────────
@login_required
@require_POST
def delete_all_contacts(request):
    """
    POST /trusted/delete-all/
    Удаляет все контакты и журнал.
    """
    TrustedContact.objects.filter(user=request.user).delete()
    ThreatLog.objects.filter(user=request.user).delete()

    return JsonResponse({
        'status': 'ok',
        'message': '🗑️ Барлық байланыстар жойылды',
    })
