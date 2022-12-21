#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import smtplib
import sys
import syslog
from dotenv import load_dotenv


def send_email(subject, text):
    '''
    Отправка сообщения по электронной почте
    '''
    
    # Загрузка файла с переменными окружения
    # !!! Данный файл должен быть добавлен в .gitignore !!!
    load_dotenv('.env_send_email')

    MAIL_SENDER_ADDRESS = os.getenv('MAIL_SENDER_ADDRESS')
    MAIL_SENDER_PASSWORD = os.getenv('MAIL_SENDER_PASSWORD')
    MAIL_SENDER_DOMAIN = os.getenv('MAIL_SENDER_DOMAIN')
    MAIL_SENDER_PORT = os.getenv('MAIL_SENDER_PORT')
    MAIL_RECEIVER_ADDRESS = os.getenv('MAIL_RECEIVER_ADDRESS')

    message = f'From: {MAIL_SENDER_ADDRESS}\nTo: {MAIL_RECEIVER_ADDRESS}\nSubject: {subject}\nContent-Type: text/plain; charset=utf-8;\n\n{text}'

    try:
        # Установка связи с SMTP сервером
        mail_server = smtplib.SMTP_SSL(MAIL_SENDER_DOMAIN, MAIL_SENDER_PORT)
        # Вывод сообщений для отладки
        # mail_server.set_debuglevel(2)
        # Отправка приветствия SMTP серверу (EHLO)
        mail_server.ehlo()
        # Вход на SMTP сервер
        mail_server.login(MAIL_SENDER_ADDRESS, MAIL_SENDER_PASSWORD)
        # Запись сообщения в syslog
        syslog.syslog(syslog.LOG_INFO, 'INFO: Login to SMTP server OK')
        # Отправка сообщения электронной почты
        mail_server.sendmail(MAIL_SENDER_ADDRESS, MAIL_RECEIVER_ADDRESS, message.encode('utf-8'))
        # Запись сообщения в syslog
        syslog.syslog(syslog.LOG_INFO, 'INFO: Send email message OK')
        # Завершение сеанса и закрытие соединения с SMTP сервером
        mail_server.quit()

    except Exception as exception_message:
        # Запись сообщения об ошибках в syslog
        syslog.syslog(syslog.LOG_ERR, 'ERROR: ' + str(exception_message))
        

def main():
    send_email('Разработка', 'Тест тест тест')


if __name__ == '__main__':
    # Обработка <Ctrl>+<C>
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
