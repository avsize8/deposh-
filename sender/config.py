import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot настройки
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Email настройки
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
DEFAULT_RECIPIENT = os.getenv('DEFAULT_RECIPIENT', '')

# Проверка обязательных переменных
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

if not EMAIL_USER or not EMAIL_PASSWORD:
    raise ValueError("EMAIL_USER и EMAIL_PASSWORD должны быть установлены в переменных окружения")

