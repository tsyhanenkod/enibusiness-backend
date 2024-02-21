from django.core.mail import send_mail
from django.conf import settings
import random

def generateOtp():
    otp=""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp


def register_mail(email, token):
    subject = 'ENI - Set password'
    message = f'''Thank you for registering with us. Please set your password by clicking on the link below:\n
    \nLink: http://{settings.DOMAIN}/set_password/{token}/\n
    \nAll the best, ENI Team!\n
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)


def otp_code_mail(email, code):
    subject = 'ENI - Reset password code'
    message = f'''Use the code below to reset your password.\n
    \nCode: {code}\n
    \nAll the best, ENI Team!\n
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)