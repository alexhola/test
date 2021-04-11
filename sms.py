import imaplib  # Подключаем библиотеку для работы по протоколу IMAP
import email  # Подключаем библиотеку для работы с email
import telebot  # подключаем библиотеку для работы с API Telegram бота

bot = telebot.TeleBot('<TOKEN_TG_Bot>')  # укажите ваш токен

mail = imaplib.IMAP4_SSL('<IMAP_ADDR>')  # Адрес IMAP сервера
mail.login('<LoGIN>', '<password>')  # Учетные данные электронной почты
mail.list()  # Смотрим на папки в ящике
mail.select('1')  # Подключаемся к папке с именем 1
result, data = mail.uid('search', None, 'UNSEEN')  # Выполняет поиск и возвращает UID писем.

i = len(data[0].split())
for x in range(i):
    latest_email_uid = data[0].split()[0]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)  # получаем сырое письмо в виде строки

for part in email_message.walk():
    if part.get_content_type() == "text/html" or part.get_content_type() == "text/plain":
        body = part.get_payload(decode=True)
        s = (email_message['Subject'])
        numb = s[5:17]  # Выделяем номер получателя 11 значный в виде 7XXXXXXXXXX с помощью среза
        mss = str(body.decode('unicode-escape'))  # декодируем тело письма и в Python3 отменяем unicode
        smss = mss[59:]  # выделяем тело СМС, а именно собственно само сообщение
        smss1 = smss.replace("Content:", "", 1)   # Убираем из тела смс, слово "Content:"
        soobsh=('Кому:  +' + numb + '\n' + 'От:  ' + smss1)  # форматируем для отправки
        bot.send_message(<CHAT_ID>, soobsh)  # укажите ваш chat_id и отправляйте в телегу ваше СМС
        #
        raw_email = email_data[0][1]
        mov, data = mail.uid('STORE', latest_email_uid, '+FLAGS', '(\Deleted)')  # Помечаем к уаделнию последнее письмо
        mail.expunge()  # очищаем корзину
        #
    else:
        continue
