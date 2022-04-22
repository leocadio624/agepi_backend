from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.comunidad.models import Alumno, Profesor

from apps.users.api.serializers import UserSerializer, TestUserSerializer, UserListSerializer


from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import string
import random



@api_view(['GET', 'POST'])
def user_api_view(request):

    
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username', 'email', 'password', 'name')
        users_serializer  = UserListSerializer(users, many = True)

        """
        Con esto se crea un nuevo usuario
        test_data = {
            'name':'develop', 
            'email':'test1@gmail.com'
        }
        test_user = TestUserSerializer(data = test_data, context = test_data)

        if test_user.is_valid():
            user_instance = test_user.save()
            print(user_instance)
        else:
            print(test_user.errors)
        """
        return Response(users_serializer.data)



    elif request.method == 'POST':


        is_student = request.data['is_student']    
        email = request.data['email']
        name = request.data['name']
        last_name = request.data['last_name']


        alumnos = Alumno.objects.filter(email = email).values('email')
        profesores = Profesor.objects.filter(email = email).values('email')

        union  = alumnos.union(profesores)
        
        if len(union) == 0:
            return Response({'message':'Tus datos no estan actualizados, favor de acudir a la CATT'}, status = status.HTTP_206_PARTIAL_CONTENT)

        
        alumnos     = Alumno.objects.filter(email = email, alta_app = True).exclude(fk_user = 0).values('id')
        profesores  = Profesor.objects.filter(email = email, alta_app = True).exclude(fk_user = 0).values('id')

        union  = alumnos.union(profesores)

        if  union:
            return Response({'message':'Este usuario ya se encuentra registrado'}, status = status.HTTP_226_IM_USED)

        code_activate = codeActivation();
        request.data['code_activate'] = code_activate

        user_serializer = UserSerializer(data = request.data)
        if  user_serializer.is_valid():

            user_serializer.save()
            sendEmailCode(name, last_name, email, code_activate, 0)

            if  is_student:
                instancia = Alumno.objects.filter(email = email, state = True).first()
            else:
                instancia = Profesor.objects.filter(email = email, state = True).first()

            instancia.fk_user = user_serializer.data['id']
            instancia.alta_app = True
            instancia.save()

            return Response({
                'message':'Se ha creado el usuario correctamente',
                'user':user_serializer.data}
                , status = status.HTTP_201_CREATED)
        return Response(user_serializer.errors)
    


    

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    user = User.objects.filter(id=pk).first()
    
    #validation
    if user:
        #retrieve
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status = status.HTTP_200_OK)
        #update
        elif request.method == 'PUT':
            
            user_serializer = UserSerializer(user, data = request.data)
            #user_serializer = TestUserSerializer(instance = user, data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status = status.HTTP_200_OK)
            return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            """
            {
                "id": 2,
                "password": "nueva_contra",
                "last_login": "2022-02-24T21:34:30.842888Z",
                "is_superuser": true,
                "username": "lalo",
                "email": "lalo@gmail.com"
            }
            """
        #delete
        elif request.method == 'DELETE':
            user = User.objects.filter(id=pk).first()
            user.delete()
            return Response({'message':'Usuario eliminado'}, status = status.HTTP_200_OK)
    return Response({'message':'No se encontro el usuario'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def activateUserApiView(request):

    if request.method == 'POST':
        pk      = request.data['id']
        code    = request.data['code']

        user            = User.objects.filter(id = pk).first()
        if  user:
            if code == user.code_activate:
                user.is_staff = True
                user.save()
                return Response({
                    'message':'Se ha activado tu cuenta correctamente'
                    }, status = status.HTTP_200_OK)
            return Response({'message':'El c&oacute;digo de activaci&oacute;n no corresponde al enviado por correo electr&oacute;nico'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message':'No se encontr&oacute; el usuario'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def sendActivateCodeApiView(request):

    if request.method == 'POST':
        pk      = request.data['id']
        user            = User.objects.filter(id = pk).first()

        if  user:
            code = codeActivation()
            sendEmailCode(user.name, user.last_name, user.email, code, 1)
            user.code_activate = code
            user.save()

            return Response({
                    'message':'Se ha reenviado el c&oacute;digo de activaci&oacute;n a tu cuenta de correo electr&oacute;nico'
                    }, status = status.HTTP_200_OK)
        return Response({'message':'No se encontr&oacute; el usuario'}, status = status.HTTP_400_BAD_REQUEST)

def codeActivation():
    length_of_string = 8
    code = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    return code


def sendEmailCode(name, last_name, receiver, code, bandera):
    receiver = 'leocadio624@gmail.com'

    host = settings.EMAIL_HOST
    sender = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    


    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Activacion cuenta'

    
    if bandera == 0:
        email_body = 'Hola '+name+' '+last_name+' tu código de activación es: '+str(code)+''
    else:
        email_body = 'Hola '+name+' '+last_name+' tu nuevo código de activación es: '+str(code)+''

    msg.attach(MIMEText(email_body, 'plain'))
    email_body_content = msg.as_string()

    server = smtplib.SMTP(host)
    server.starttls()

    server.login(sender, password)
    server.sendmail(sender, receiver, email_body_content)
    server.quit()






