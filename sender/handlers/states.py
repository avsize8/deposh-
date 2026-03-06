from aiogram.fsm.state import State, StatesGroup


class EmailStates(StatesGroup):
    """Состояния FSM для процесса отправки email"""
    waiting_email = State()
    waiting_subject = State()
    waiting_html = State()

