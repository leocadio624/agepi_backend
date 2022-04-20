from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.protocol.models import Protocol
from apps.users.models import User

from pathlib import Path
import os
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.api.serializers import CustomTokenObtainPairSerializer, CustomUserSerializer

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(
            username = username,
            password = password
        )
        print(user)
        
        if  user:
            login_serializer = self.serializer_class(data = request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token' : login_serializer.validated_data.get('access'),
                    'refresh_token':login_serializer.validated_data.get('refresh'),
                    'user':user_serializer.data,
                    }, status = status.HTTP_200_OK)

            return Response({'message':'Contraseña o nombre de usuario incorrectos'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Contraseña o nombre de usuario incorrectos'}, status = status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id = request.data.get('user', 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message':'Sesion cerrada correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe este usuario'}, status = status.HTTP_400_BAD_REQUEST)        



class DownloadFile(APIView):
    def post(self, request, *args, **kwargs):    
        path = request.data['pathProtocol']
        base = Path(__file__).resolve().parent.parent.parent
        pathFile  = str(base) + path

        document = open(pathFile, 'rb')

        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment'
        return response