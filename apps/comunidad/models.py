from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


class ProgramaAcademico(models.Model):
	id = models.IntegerField(primary_key = True)
	programa = models.CharField('Descripccion del programa academico', max_length = 50, blank = False, null = False, unique = False)
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
	fk_programa = models.ForeignKey(ProgramaAcademico, on_delete = models.CASCADE, verbose_name = 'pk de programa academico', null = False, blank = False)
	fk_user = models.IntegerField(default = 0)
	alta_app = models.BooleanField('Dado de alta en aplicacion', default = False)
	email = models.EmailField('Correo Electronico', max_length = 50,  blank = False, unique = False)
	boleta = models.CharField('Boleta', 			max_length = 50,  blank = False, unique = True)
	

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
	departamento = models.CharField('departamento', max_length = 100, blank = False, null = False, unique = False)
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


class Academia(models.Model):
	id = models.IntegerField(primary_key = True)
	academia = models.CharField('academia', max_length = 100, blank = False, null = False, unique = False)
	fk_departamento = models.ForeignKey(Departamento, on_delete = models.CASCADE, verbose_name = 'fk_departamento', null = False, blank = False)
	historical = HistoricalRecords()


	@property
	def _history_user(self):
	    return self.change_by

	@_history_user.setter
	def _history_user(self, vale):
	    self.changed_by = value

	class Meta:
	    verbose_name = 'Academias'
	    verbose_name_plural = 'Acedemias'

	def __str__(self):
	    return self.academia







class Profesor(BaseModel):
	fk_academia = models.ForeignKey(Academia, on_delete = models.CASCADE, verbose_name = 'fk_academia', null = False, blank = False)
	fk_user = models.IntegerField(default = 0)
	alta_app = models.BooleanField('Dado de alta en aplicacion', default = False)
	email = models.EmailField('Correo Electronico', max_length = 50, unique = True)
	noEmpleado = models.CharField('Numero de noEmpleado', max_length = 50, blank = True, null = True)
	
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