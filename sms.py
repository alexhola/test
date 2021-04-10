import imaplib
import email
import telebot

bot = telebot.TeleBot('<TOKEN_BOT>')  # ������� ��� �����

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('<account>@gmail.com', '<password>')  # ��� ����� ������� @gmail
mail.list()  # ������� �� ����� � �����
mail.select('INBOX')  # ������������ � ����� ��������
result, data = mail.uid('search', None, 'UNSEEN')  # �������� �������������

i = len(data[0].split())
for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = email_data[0][1]
    mail.store(latest_email_uid, '+FLAGS', 'Deleted')  # ������� ���� �� ���� ��������� ��������
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)  # �������� ����� ������ � ���� ������

for part in email_message.walk():
    if part.get_content_type() == "text/html" or part.get_content_type() == "text/plain":
        body = part.get_payload(decode=True)
        s = (email_message['Subject'])
        mss = str(body.decode('unicode-escape'))  # ���������� ���� ������ � � Python3 �������� unicode
        abon = mss[45:58]  # �������� ����� �����������
        smss = mss[59:]  # �������� ���� ���, � ������ ���������� ���� ���������
        soobsh = ('��:  ' + abon + ' \n' + '�����:  ' + smss)  # ����������� ��� ��������
        bot.send_message(<chat_id, soobsh)  # ������� ��� chat_id � ����������� � ������ ���� ���
    else:
        continue
