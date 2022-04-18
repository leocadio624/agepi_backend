from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


class ProgramaAcademico(models.Model):
	id = models.IntegerField(primary_key = True)
	programa = models.CharField('Descripccion del programa academico', max_length = 255, blank = False, null = False, unique = False)
	historical = HistoricalRecords()


	@property
	def _history_user(self):
	    return self.change_by

	@_history_user.setter
	def _history_user(self, vale):
	    self.changed_by = value

	class Meta:
	    verbose_name = 'Programa Academico'
	    verbose_name_plural = 'Programas Academicos'

	def __str__(self):
	    return self.programa



class Alumno(BaseModel):
	fk_programa = models.ForeignKey(ProgramaAcademico, on_delete = models.CASCADE, verbose_name = 'pk de alumno', null = False, blank = False)
	fk_user = models.IntegerField(default = 0)
	alta_app = models.BooleanField('Dado de alta en aplicacion', default = False)
	email = models.EmailField('Correo Electronico', max_length = 255,  blank = False, unique = False)
	boleta = models.CharField('Boleta', 			max_length = 255,  blank = False, unique = True)
	

	@property
	def _history_user(self):
	    return self.change_by

	@_history_user.setter
	def _history_user(self, vale):
	    self.changed_by = value

	class Meta:
	    verbose_name = 'Alumno'
	    verbose_name_plural = 'Alumnos'

	def __str__(self):
	    return self.email



class Departamento(models.Model):
	id = models.IntegerField(primary_key = True)
	departamento = models.CharField('Departamento escolar', max_length = 255, blank = False, null = False, unique = False)
	historical = HistoricalRecords()


	@property
	def _history_user(self):
	    return self.change_by

	@_history_user.setter
	def _history_user(self, vale):
	    self.changed_by = value

	class Meta:
	    verbose_name = 'Departamento'
	    verbose_name_plural = 'Departamentos'

	def __str__(self):
	    return self.departamento


class Profesor(BaseModel):
	fk_departamento = models.ForeignKey(Departamento, on_delete = models.CASCADE, verbose_name = 'pk de profesor', null = False, blank = False)
	fk_user = models.IntegerField(default = 0)
	alta_app = models.BooleanField('Dado de alta en aplicacion', default = False)
	email = models.EmailField('Correo Electronico', max_length = 255, unique = True)
	noEmpleado = models.CharField('Numero de noEmpleado', max_length = 255, blank = True, null = True)
	
	@property
	def _history_user(self):
	    return self.change_by

	@_history_user.setter
	def _history_user(self, vale):
	    self.changed_by = value

	class Meta:
	    verbose_name = 'Profesor'
	    verbose_name_plural = 'Profesores'

	def __str__(self):
	    return self.email