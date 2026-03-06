import logging
import re
from telegram import Update
from telegram.ext import ContextTypes

from utils.email_sender import email_sender
from config import DEFAULT_RECIPIENT

logger = logging.getLogger(__name__)


def is_valid_email(email: str) -> bool:
    """Проверяет валидность email адреса"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений"""
    user_id = update.effective_user.id
    text = update.message.text
    
    # Получаем текущее состояние пользователя
    state = context.user_data.get('state')
    
    if state == 'waiting_email':
        # Проверяем валидность email
        if is_valid_email(text):
            context.user_data['email'] = text
            context.user_data['state'] = 'waiting_subject'
            await update.message.reply_text(f"✅ Email сохранен: {text}\n\n📝 Теперь введите тему письма:")
        else:
            await update.message.reply_text("❌ Неверный формат email. Пожалуйста, введите корректный email адрес.")
    
    elif state == 'waiting_subject':
        # Сохраняем тему
        context.user_data['subject'] = text
        context.user_data['state'] = 'waiting_html'
        await update.message.reply_text(
            "✅ Тема сохранена.\n\n"
            "📄 Теперь отправьте HTML текст письма.\n"
            "💡 Вы можете использовать HTML теги для форматирования."
        )
    
    elif state == 'waiting_html':
        # Сохраняем HTML контент и отправляем письмо
        html_content = text
        
        # Обертываем в базовую HTML структуру, если нужно
        if not html_content.strip().startswith('<'):
            html_content = f"<html><body>{html_content}</body></html>"
        
        email = context.user_data.get('email')
        subject = context.user_data.get('subject')
        
        if not email or not subject:
            await update.message.reply_text("❌ Ошибка: не хватает данных. Начните заново с /send")
            context.user_data['state'] = None
            return
        
        # Отправляем письмо
        await update.message.reply_text("⏳ Отправляю письмо...")
        
        sender_name = f"{update.effective_user.first_name} {update.effective_user.last_name or ''}".strip()
        success = email_sender.send_html_email(
            recipient=email,
            subject=subject,
            html_content=html_content,
            sender_name=sender_name
        )
        
        if success:
            await update.message.reply_text(
                f"✅ Письмо успешно отправлено!\n\n"
                f"📧 Получатель: {email}\n"
                f"📝 Тема: {subject}"
            )
        else:
            await update.message.reply_text(
                "❌ Ошибка при отправке письма.\n"
                "Проверьте логи или настройки SMTP сервера."
            )
        
        # Сбрасываем состояние
        context.user_data['state'] = None
        context.user_data['email'] = None
        context.user_data['subject'] = None
        context.user_data['html_content'] = None
    
    else:
        # Если состояние не установлено, просто отвечаем
        await update.message.reply_text(
            "👋 Привет! Используйте /start для начала работы или /send для отправки письма."
        )

