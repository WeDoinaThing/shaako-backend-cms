import uuid


def get_random_id(len=10):
    return uuid.uuid4().hex[:len].upper()


import threading
from django.core.mail import send_mail, send_mass_mail


class EmailThread(threading.Thread):
    def __init__(self, mail_content):
        self.mail_content = mail_content
        threading.Thread.__init__(self)

    def run(self):
        print("Sending mail")
        send_mass_mail((self.mail_content,), fail_silently=False)
        print("Mail sent")


def send_async_mail(mail_content):
    EmailThread(mail_content).start()
