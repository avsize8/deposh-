import logging
import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.states import EmailStates
from utils.email_sender import email_sender

logger = logging.getLogger(__name__)

router = Router()


def is_valid_email(email: str) -> bool:
    """Проверяет валидность email адреса"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@router.message(EmailStates.waiting_email)
async def handle_email_input(message: Message, state: FSMContext):
    """Обработчик ввода email"""
    text = message.text
    
    # Проверяем валидность email
    if is_valid_email(text):
        await state.update_data(email=text)
        await state.set_state(EmailStates.waiting_subject)
        await message.answer(f"✅ Email сохранен: {text}\n\n📝 Теперь введите тему письма:")
    else:
        await message.answer("❌ Неверный формат email. Пожалуйста, введите корректный email адрес.")


@router.message(EmailStates.waiting_subject)
async def handle_subject_input(message: Message, state: FSMContext):
    """Обработчик ввода темы письма"""
    text = message.text
    
    # Сохраняем тему
    await state.update_data(subject=text)
    await state.set_state(EmailStates.waiting_html)
    await message.answer(
        "✅ Тема сохранена.\n\n"
        "📄 Теперь отправьте HTML текст письма.\n"
        "💡 Вы можете использовать HTML теги для форматирования."
    )


@router.message(EmailStates.waiting_html)
async def handle_html_input(message: Message, state: FSMContext):
    """Обработчик ввода HTML контента и отправка письма"""
    html_content = message.text
    
    # Получаем данные из состояния
    data = await state.get_data()
    email = data.get('email')
    subject = data.get('subject')
    
    if not email or not subject:
        await message.answer("❌ Ошибка: не хватает данных. Начните заново с /send")
        await state.clear()
        return
    
    # Обертываем в базовую HTML структуру, если нужно
    if not html_content.strip().startswith('<'):
        html_content = f"<html><body>{html_content}</body></html>"
    
    # Отправляем письмо
    await message.answer("⏳ Отправляю письмо...")
    
    sender_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    success = email_sender.send_html_email(
        recipient=email,
        subject=subject,
        html_content=html_content,
        sender_name=sender_name
    )
    
    if success:
        await message.answer(
            f"✅ Письмо успешно отправлено!\n\n"
            f"📧 Получатель: {email}\n"
            f"📝 Тема: {subject}"
        )
    else:
        await message.answer(
            "❌ Ошибка при отправке письма.\n"
            "Проверьте логи или настройки SMTP сервера."
        )
    
    # Сбрасываем состояние
    await state.clear()


@router.message()
async def handle_other_messages(message: Message):
    """Обработчик всех остальных сообщений"""
    await message.answer(
        "👋 Привет! Используйте /start для начала работы или /send для отправки письма."
    )
