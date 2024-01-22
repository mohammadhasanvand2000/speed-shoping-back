from django.core.mail import send_mail
from django.conf import settings

class Util:
    @staticmethod
    def send_email(data):
        subject = data['email_subject']
        message = data['email_body']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [data['to_email']]
        send_mail(subject, message, email_from, recipient_list)