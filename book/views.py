from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import User


class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Вы успешно зарегистрировались", status=201)

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotSerializer)
    def post(self, request):
        data = request.POST
        serializer = ForgotSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = "Please, confirm your email"
            return Response(message)

class DeleteUserView(APIView):
    def delete(self, request,email):
        user = get_object_or_404(User, email=email)
        print(user)
        print(request.user)
        if request.user.is_staff:
            user.delete()
            return Response(status=204) 
        return Response(status=403)

class NewPasswordView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        new_password = user.generate_activation_code()
        user.set_password(new_password)
        user.save()
        return Response(f"Your new password is {new_password}")

@api_view(['GET'])
def activate_view(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True # делаем активным
    user.activation_code = '' # удаляем активационный код
    user.save()
    return Response('Вы успешно активировали аккаунт', status=200)

        