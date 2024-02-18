from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class SignupView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class SetPasswordView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class ForgotPasswordView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class OtpVerificationView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)


class SetNewPasswordView(GenericAPIView):
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)