from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), 'signup'),
    path('set_password/', SetPasswordView.as_view(), 'set_password'),

    path('login/', LoginView.as_view(), 'login'),
    path('logout/', LogoutView.as_view(), 'logout'),

    path('forgot_password/', ForgotPasswordView.as_view(), 'forgot_password'),
    path('otp_verification/', OtpVerificationView.as_view(), 'otp_verification'),
    path('set_new_password/', SetNewPasswordView.as_view(), 'set_new_password'),
]
