import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.states import EmailStates
from config import DEFAULT_RECIPIENT

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "/start")
async def start_command(message: Message):
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
    await message.answer(welcome_text)


@router.message(F.text == "/help")
async def help_command(message: Message):
    """Обработчик команды /help"""
    help_text = """
📖 Справка по использованию бота:

1️⃣ Отправьте команду /send
2️⃣ Бот попросит ввести email получателя
   (или отправьте /skip для использования дефолтного)
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
    await message.answer(help_text)


@router.message(F.text == "/send")
async def send_command(message: Message, state: FSMContext):
    """Обработчик команды /send - начинает процесс отправки письма"""
    # Инициализируем состояние для пользователя
    await state.set_state(EmailStates.waiting_email)
    await state.update_data(email=None, subject=None, html_content=None)
    
    if DEFAULT_RECIPIENT:
        text = f"📧 Введите email получателя (или отправьте /skip для использования дефолтного: {DEFAULT_RECIPIENT}):"
    else:
        text = "📧 Введите email получателя:"
    
    await message.answer(text)


@router.message(F.text == "/skip")
async def skip_email(message: Message, state: FSMContext):
    """Пропустить ввод email и использовать дефолтный"""
    from config import DEFAULT_RECIPIENT
    
    current_state = await state.get_state()
    
    # Проверяем, что мы в состоянии ожидания email
    if current_state != EmailStates.waiting_email:
        await message.answer("❌ Команда /skip доступна только при вводе email получателя.")
        return
    
    if not DEFAULT_RECIPIENT:
        await message.answer("❌ Дефолтный email не настроен. Пожалуйста, введите email получателя.")
        return
    
    await state.update_data(email=DEFAULT_RECIPIENT)
    await state.set_state(EmailStates.waiting_subject)
    await message.answer(f"✅ Используется дефолтный email: {DEFAULT_RECIPIENT}\n\n📝 Теперь введите тему письма:")
