import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.email_sender import email_sender
from config import DEFAULT_RECIPIENT

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
👋 Привет! Я бот для отправки HTML писем на email.

📋 Доступные команды:
/start - Показать это сообщение
/send - Отправить HTML письмо
/help - Справка по использованию

💡 Использование:
1. Отправьте команду /send
2. Введите email получателя (или используйте дефолтный)
3. Введите тему письма
4. Отправьте HTML текст письма
    """
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📖 Справка по использованию бота:

1️⃣ Отправьте команду /send
2️⃣ Бот попросит ввести email получателя
   (или нажмите Enter для использования дефолтного)
3️⃣ Введите тему письма
4️⃣ Отправьте HTML текст письма

📝 Пример HTML:
<html>
<body>
<h1>Привет!</h1>
<p>Это <b>HTML</b> письмо.</p>
</body>
</html>

⚠️ Убедитесь, что HTML валидный!
    """
    await update.message.reply_text(help_text)


async def send_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /send - начинает процесс отправки письма"""
    user_id = update.effective_user.id
    
    # Инициализируем состояние для пользователя
    context.user_data['state'] = 'waiting_email'
    context.user_data['email'] = None
    context.user_data['subject'] = None
    context.user_data['html_content'] = None
    
    if DEFAULT_RECIPIENT:
        text = f"📧 Введите email получателя (или нажмите /skip для использования дефолтного: {DEFAULT_RECIPIENT}):"
    else:
        text = "📧 Введите email получателя:"
    
    await update.message.reply_text(text)


async def skip_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пропустить ввод email и использовать дефолтный"""
    from config import DEFAULT_RECIPIENT
    
    if not DEFAULT_RECIPIENT:
        await update.message.reply_text("❌ Дефолтный email не настроен. Пожалуйста, введите email получателя.")
        return
    
    context.user_data['email'] = DEFAULT_RECIPIENT
    context.user_data['state'] = 'waiting_subject'
    await update.message.reply_text(f"✅ Используется дефолтный email: {DEFAULT_RECIPIENT}\n\n📝 Теперь введите тему письма:")

