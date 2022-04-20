from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'name', 'last_name', 'rol_user', 'is_staff')

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'


    """
    def validate_email(self, value):
        print("validate email")
        return value

    """
    def validate(self, data):
        return data


    #Sobreescribiendo estas dos funciones se encripta el campo password
    #en la creacion y actualizacion de usuarios
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    

    

    def to_representation(self, instance):
        return{
            'id':instance['id'],
            'username':instance['username'],
            'email':instance['email'],
            'password':instance['password']
        }


class TestUserSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length = 200)
    email = serializers.EmailField()

    def validate_name(self, value):
        """
        if 'develop' in value:
            raise serializers.ValidationError('Error, no puede existir un usuario con este nombre')
        """
        return value

    def validate_email(self, value):
        #print("validate email")
        print(value)
        """
        if value == '':
            raise serializers.ValidationError('Tiene que inidicar un correo electronico')

        if self.validate_name(self.context['name']) in value:
            raise serializers.ValidationError('El email no pude contener el nombre')
        """
        return value

    def validate(self, data):
        #print("validate")
        return data

    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        print( validated_data.get('name', instance.name) )
        print( validated_data.get('email', instance.email) )
        instance.save()
        return instance