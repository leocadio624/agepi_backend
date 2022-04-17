from rest_framework import serializers
from apps.comunidad.models import Alumno, Profesor


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')

    """
    """
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_programaAcademico':instance.fk_programa.id,
            'fk_user':instance.fk_user,
            'email':instance.email,
            'boleta':instance.boleta
        }

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'fk_departamento':instance.fk_departamento.id,
            'fk_user':instance.fk_user,
            'email':instance.email,
            'noEmpleado':instance.noEmpleado
        }
    """
    """
        
        

    
