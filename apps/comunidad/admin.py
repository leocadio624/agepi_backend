from django.contrib import admin
from apps.comunidad.models import ProgramaAcademico, Alumno, Departamento, Profesor

admin.site.register(ProgramaAcademico)
admin.site.register(Alumno)

admin.site.register(Departamento)
admin.site.register(Profesor)



