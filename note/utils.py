from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from note.models import *
from django.utils import timezone
from datetime import datetime, time, timedelta
def sendEmailToClient(otp, email):
    subject = "Password Recovery Mail From Your Diary!!"
    message = f"Your Password Generation OTP is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def sendMailWithAttachment():
    mail = EmailMessage(
        subject = "See this attachment",
        body = 'Helloooowwwwwwwwww',
        to = ['22981a4617@raghuenggcollege.in'],
        from_email = settings.EMAIL_HOST_USER
    )
    file_path = f"{settings.BASE_DIR}/manage.py"
    mail.attach_file(file_path)
    mail.send()


def deleteotpreqs(user):
    threshold = timezone.now() - timedelta(days=1)
    OTPRequest.objects.filter(user = user, timestamp__lt = threshold).delete()