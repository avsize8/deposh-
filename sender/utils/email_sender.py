import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

from config import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD

logger = logging.getLogger(__name__)


class EmailSender:
    """Класс для отправки HTML писем через SMTP"""
    
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.email_user = EMAIL_USER
        self.email_password = EMAIL_PASSWORD
    
    def send_html_email(
        self,
        recipient: str,
        subject: str,
        html_content: str,
        sender_name: Optional[str] = None
    ) -> bool:
        """
        Отправляет HTML письмо на указанный email
        
        Args:
            recipient: Email получателя
            subject: Тема письма
            html_content: HTML содержимое письма
            sender_name: Имя отправителя (опционально)
        
        Returns:
            True если письмо отправлено успешно, False в противном случае
        """
        try:
            # Создаем сообщение
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{sender_name} <{self.email_user}>" if sender_name else self.email_user
            msg['To'] = recipient
            
            # Добавляем HTML контент
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Отправляем письмо
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Включаем TLS шифрование
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Письмо успешно отправлено на {recipient}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("Ошибка аутентификации SMTP. Проверьте EMAIL_USER и EMAIL_PASSWORD")
            return False
        except smtplib.SMTPRecipientsRefused:
            logger.error(f"Неверный адрес получателя: {recipient}")
            return False
        except Exception as e:
            logger.error(f"Ошибка при отправке письма: {str(e)}")
            return False


# Создаем глобальный экземпляр
email_sender = EmailSender()

