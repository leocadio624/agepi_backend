from rest_framework import serializers
from apps.comunidad.models import Alumno, ProgramaAcademico, Profesor


class ProgramaAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaAcademico
        fields = '__all__'
        

    def to_representation(self, instance):
        return {
        'id'        : instance.id,
        'programa'  : instance.programa
        }



class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def validate(self, data):
        return data
    


    def to_representation(self, instance):

        if instance.alta_app and instance.fk_user != 0:
            estado = 'Dado de alta'
        else:
            estado = 'Disponible para registro'

        return {
            'id':instance.id,
            'estado':estado,
            'fk_programaAcademico':instance.fk_programa.id,
            'programaAcademico':instance.fk_programa.programa,
            'fk_user':instance.fk_user,
            'email':instance.email,
            'boleta':instance.boleta
        }




class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    def to_representation(self, instance):
        
        if instance.alta_app and instance.fk_user != 0:
            estado = 'Dado de alta'
        else:
            estado = 'Disponible para registro'

        return {
            'id':instance.id,
            'estado': estado,
            'academia':instance.fk_academia.academia,
            'fk_user':instance.fk_user,
            'email':instance.email,
            'noEmpleado':instance.noEmpleado
        }
    
    
        
        

    
