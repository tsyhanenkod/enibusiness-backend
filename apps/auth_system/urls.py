from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('set_password/<str:token>/', SetPasswordView.as_view(), name='set_password'),

    path('signup_request/', SignupRequestView.as_view(), name='signup_request'),
    path('signup_request_accept/', SignupAcceptRequestView.as_view(), name='signup_request_accept'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('otp_verification/', OtpVerificationView.as_view(), name='otp_verification'),
    path('set_new_password/', SetNewPasswordView.as_view(), name='set_new_password'),
]
