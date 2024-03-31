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


def request_signup_success(email, token):
    subject = 'ENI - Signup Request'
    message = f'''Your registration request accepted by admin. Please set your password by clicking on the link below:\n
    \nLink: http://{settings.DOMAIN}/set_password/{token}/\n
    \nAll the best, ENI Team!\n
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)


def request_signup_rejected(email):
    subject = 'ENI - Signup Request'
    message = f'''Your registration request rejected by admin.\n
    \nAll the best, ENI Team!\n
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)


def request_signup_admin_nitification(email, first_name, last_name, phone, location, business):
    subject = f'ENI - Signup Request'
    message = f'''User {first_name} with email {email} sent signup request.\n
    \nUser {first_name} {last_name}: 
    \nEmail: {email}
    \nPhone: {phone}
    \nLocation: {location}
    \nBusiness: {business}\n 
    \nAccept it or decline in Admin tools page\n

    \nAll the best, ENI App!\n
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]

    send_mail(subject, message, email_from, recipient_list)