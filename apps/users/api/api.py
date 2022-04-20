from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.comunidad.models import Alumno, Profesor

from apps.users.api.serializers import UserSerializer, TestUserSerializer, UserListSerializer



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

        
        user_serializer = UserSerializer(data = request.data)
        if  user_serializer.is_valid():

            user_serializer.save()

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
    #queryset
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
            #print(user)
            return Response({'message':'Usuario eliminado'}, status = status.HTTP_200_OK)
    return Response({'message':'No se encontro el usuario'}, status = status.HTTP_400_BAD_REQUEST)

"""
Para probar la creacion de usuarios
{
    "password": "contrasenia",
    "last_login": "2022-02-24T21:34:30.842888Z",
    "is_superuser": true,
    "username": "lalo",
    "email": "lalo@gmail.com",
    "name": "josue eduardo",
    "last_name": "bernal leocadio",
    "image": null,
    "is_active": true,
    "is_staff": true,
    "groups": [],
    "user_permissions": []
}
"""
