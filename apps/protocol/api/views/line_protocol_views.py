from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.protocol.api.serializers.protocol_serializers import ProtocolSerializer, ProtocolLineaSerializer, SelectProtocoloSerializer, EvaluacionSerializer, PreguntaSerializer
from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.firma.api.serializers.firma_serializers import FirmaProtocoloLineaSerializer
from apps.comunidad.models import Profesor, Academia

import pdfkit
import base64

import pytz
from django.utils import timezone

import os
from pathlib import Path
from django.http import HttpResponse
from wsgiref.util import FileWrapper



class LineProtocolStartViewSet(viewsets.ModelViewSet):
	serializer_class = ProtocolLineaSerializer
	
	def list(self, request):

		pk_user = request.GET["pk_user"]
		team = TeamMemberSerializer.Meta.model.objects.filter(fk_user = pk_user, solicitudEquipo = 2, state = True).first()

		if team is None:
			return Response([], status = status.HTTP_200_OK)	
		
		fk_team = team.fk_team.id
		protocol_serializer = ProtocolLineaSerializer(ProtocolLineaSerializer.Meta.model.objects.filter(fk_team = fk_team, state = True), many = True)

		return Response(protocol_serializer.data, status = status.HTTP_200_OK)

class getIntegrantesViewSet(viewsets.ModelViewSet):

	def getIntegrantes(self, fk_team):
		return TeamMemberSerializer.Meta.model.objects.filter(fk_team = fk_team, solicitudEquipo = 2, state = True)

	
	def list(self, request):
		fk_team = request.GET["fk_team"]
		integrantes_serializer = TeamMemberSerializer(self.getIntegrantes(fk_team), many = True) 
		return Response(integrantes_serializer.data, status = status.HTTP_200_OK)


class getFirmasViewSet(viewsets.ModelViewSet):

	def getFirmas(self, fk_protocol):
		return FirmaProtocoloLineaSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True)

	def list(self, request):
		fk_protocol = request.GET["fk_protocol"]
		firmas_serializer = FirmaProtocoloLineaSerializer(self.getFirmas(fk_protocol), many = True) 
		return Response(firmas_serializer.data, status = status.HTTP_200_OK)

class verEvaluacionSinodalViewSet(viewsets.ModelViewSet):
	def convertUTC(self, date):
		fmt = '%d/%m/%Y %H:%M'
		utc = date.replace(tzinfo=pytz.UTC)
		localtz = utc.astimezone(timezone.get_current_timezone())
		return localtz.strftime('%m/%d/%Y %H:%M:%S')

	def get_image_file_as_base64_data(self, ruta):
		with open(ruta, 'rb') as image_file:
			salida = base64.b64encode(image_file.read())
			salida = salida.decode('UTF-8')
			return salida

	def create(self, request):
		fk_seleccion 	= request.data['fk_seleccion']
		fk_protocol 	= request.data['fk_protocol']
		fk_user 		= request.data['fk_user']
		
		protocol_serializer = ProtocolSerializer(ProtocolSerializer.Meta.model.objects.filter(id=fk_protocol).first(), many = False)
		fileProtocol = protocol_serializer.data['fileProtocol']

		base            = Path(__file__).resolve().parent.parent.parent.parent.parent
		pathFile        = str(base) + str(fileProtocol)
		#dir_pdf         = os.path.dirname(os.path.realpath(pathFile)) + '/evaluaciones/'+str(fk_user)+'/evaluacion.pdf'
		dir_pdf         = os.path.dirname(os.path.realpath(pathFile)) + '/evaluacion_'+str(fk_user)+'_.pdf'
		


		select = SelectProtocoloSerializer.Meta.model.objects.filter(id=fk_seleccion).first()
		numero = select.fk_protocol.number
		titulo = select.fk_protocol.title
		nombre_sinodal = select.fk_user.name + ' ' +select.fk_user.last_name
		contacto = select.fk_user.email
		
	
		evaluacion = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion = fk_seleccion).first()

		pk_evaluacion 		= evaluacion.id
		fecha_evaluacion 	= self.convertUTC(evaluacion.created_date)
		dictamen 			= evaluacion.dictamen
		version 			= evaluacion.version
		recomendaciones 	= evaluacion.observacion_general

		preguntas =  PreguntaSerializer(PreguntaSerializer.Meta.model.objects.filter(fk_evaluacion = pk_evaluacion), many = True)
		preguntas_list = preguntas.data

		profesor = Profesor.objects.filter(fk_user = fk_user, state = True).first()
		
		academia = profesor.fk_academia.academia
		departamento = profesor.fk_academia.fk_departamento.departamento

		
		pie_evaluacion = str(base) + '/pie_evaluacion.PNG'
		data_footer    = self.get_image_file_as_base64_data(pie_evaluacion)

		htmlstr = '<!doctype html>'
		htmlstr += '<html lang="en">'
		htmlstr += '<head>'
		htmlstr += '<meta charset="utf-8">'
		htmlstr += '<meta name="viewport" content="width=device-width, initial-scale=1">'
		htmlstr += '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">'
		htmlstr += '</head>'
		htmlstr += '<style>'
		htmlstr += 'table, th, td {'
		htmlstr += 'border: 1px solid black;'
		htmlstr += 'padding:7px;'
		htmlstr += '}'
		htmlstr += '.up_table{'
		htmlstr +=     'border-left: 2px solid black;'
		htmlstr +=     'border-top: 2px solid black;'
		htmlstr +=     'border-right: 2px solid black;'
		htmlstr += '}'
		htmlstr += '.center_table{'
		htmlstr += 		'border-left: 2px solid black;'
		htmlstr += 		'border-right: 2px solid black;'
		htmlstr += '}'
		htmlstr += '.down_table{'
		htmlstr +=     'border-left: 2px solid black;'
		htmlstr +=     'border-bottom: 2px solid black;'
		htmlstr +=     'border-right: 2px solid black;'
		htmlstr += '}'
		htmlstr += '.fuente{'
		htmlstr +=    'font-size:13px;'
		htmlstr +=    'text-align:justify;'
		htmlstr += '}'


		htmlstr += '.no_border{'
		htmlstr += 		'border-left:2px solid black!important;'
		htmlstr += 		'border-right:2px solid black!important;'
		htmlstr += 		'border-bottom:0px!important;'
		htmlstr += 		'border-top:0px!important;'
		htmlstr += '}'


		htmlstr += '.container{'
		htmlstr += 'margin-left: 30px!important;'
		htmlstr += 'margin-right: 30px!important;'
		htmlstr += 'max-width: 950px!important;'
		htmlstr += '}'
		htmlstr += '</style>'
		htmlstr += '<body>'
		htmlstr += '<div class="row">'
		htmlstr += '<div class="col-12 d-flex justify-content-center" style = "margin-top:35px;">'
		htmlstr += '<h4><strong>EVALUACI&Oacute;N PARA PROPUESTAS DE TRABAJO TERMINAL</strong></h4>'
		htmlstr += '</div>'
		htmlstr += '</div>'
		htmlstr += '<div class = "container">'
		htmlstr += '<table  width = "100%" style = "margin-top:15px;" >'
		htmlstr += '<tr class = "up_table" >'
		htmlstr += 		'<td colspan = "4" class= "fuente" ><strong>NO. DE REGISTRO DEL TT:&nbsp;</strong>'+numero+'</td>'
		htmlstr += '</tr>'
		htmlstr += '<tr class = "center_table">'
		htmlstr +=  	'<td colspan = "4" class= "fuente" ><strong>T&Iacute;TULO DE TT:&nbsp;</strong>'+titulo+'</td>'
		htmlstr += '</tr>'
		htmlstr += '<tr class = "down_table" >'
		htmlstr += 		'<td width = "50%" class= "fuente" ><strong>FECHA DE EVALUACI&OacuteN:&nbsp;</strong>'+fecha_evaluacion+'</td>'
		htmlstr += 		'<td width = "34%" class= "fuente" >NO. DE VERSI&Oacute;N:</td>'
		if version == 1:
			htmlstr +=     	'<td width = "8%"  class= "fuente" > 1a:&nbsp;&nbsp;&nbsp;&nbsp<strong style = "font-size:15px!important;" >X</strong></td>'
			htmlstr +=     	'<td width = "8%"  class= "fuente" > 2a:</td>'
		else:
			htmlstr +=     	'<td width = "8%"  class= "fuente" > 1a:</td>'
			htmlstr +=     	'<td width = "8%"  class= "fuente" > 2a:&nbsp;&nbsp;&nbsp;&nbsp<strong style = "font-size:15px!important;" >X</strong></td>'

		htmlstr += '</tr>'
		htmlstr += '</table>'
		htmlstr += '<table  width = "100%" style = "" >'
		htmlstr += 		'<tr class = "center_table" >'
		htmlstr += 			'<td width = "50%" class= "fuente text-center" ><strong>PREGUNTA</strong></td>'
		htmlstr += 			'<td width = "5%" class= "fuente text-center" ><strong>SI</strong></td>'
		htmlstr += 			'<td width = "5%" class= "fuente text-center" ><strong>NO</strong></td>'
		htmlstr += 			'<td width = "40%" class= "fuente text-center" ><strong>OBSERVACIONES</strong></td>'
		htmlstr += 		'</tr>'

		preguntas = [
		'<strong>1. T&iacute;tulo de TT.</strong><br>¿El t&iacute;tulo corresponde el t&iacute;tulo esperado?',
		'<strong>2. Resumen.</strong><br>¿El resumen expresa claramente la propuesta del TT, su importancia y aplicaci&oacute;n?',
		'<strong>3. Introducci&oacute;n.</strong><br>¿Las palabras clave han sido clasificadas adecuadamente?',
		'<strong>4. Justificaci&oacute;n.</strong><br>¿La presentaci&oacute;n del problema a resolver es comprensible?',
		'<strong>5. Objetivo.</strong><br>¿El objetivo es preciso y relevante?',
		'<strong>6. Planteamiento.</strong><br>¿El planteamiento del problema y la tentativa soluci&oacute;n descrita son claros?',
		'<strong>7. Justificaci&oacute;n.</strong><br>¿Sus contribuciones o beneficios est&aacute;n completamente justificados?<br>''Originalidad, vinculaci&oacute;n con poblaci&oacute;n usuaria potencial, utilidad de los resultados,complejidad en su elaboraci&oacute;n a nivel ingeniería, mejoramiento de lo existente, etc.',
		'<strong>8. Resultados o productos esperados.</strong><br>¿Su viabilidad es adecuada?<br>Tiempos, recursos humanos y materiales, alcances, costos y otros puntos que puedan impedir la culminaci&oacute;n exitosa del trabajo.',
		'<strong>9. Metodolog&iacute;a.</strong><br>¿La propuesta metodol&oacute;gica es pertinente?',
		'<strong>10. Cronograma.</strong><br>¿El calendario de actividades por estudiante es adecuado?'
		]

		indice = 0
		for i in preguntas_list:
			htmlstr += 		'<tr class = "center_table" >'
			htmlstr += 			'<td width = "50%" class= "fuente text-left" >'+preguntas[indice]+'</td>'

			if i['estado'] == True:
				htmlstr += 			'<td width = "5%"  class= "fuente text-center" ><strong style = "font-size:15px!important;" >X</strong></td>'
				htmlstr += 			'<td width = "5%"  class= "fuente text-center" ></td>'
			else:
				htmlstr += 			'<td width = "5%"  class= "fuente text-center" ></td>'
				htmlstr += 			'<td width = "5%"  class= "fuente text-center" ><strong style = "font-size:15px!important;" >X</strong></td>'

			htmlstr += 			'<td width = "40%" class= "fuente text-left" >'+i['observacion']+'</td>'
			htmlstr += 		'</tr>'
			indice += 1

		htmlstr += '</table>'
		htmlstr += '<table  width = "100%" style = "" >'
		htmlstr += 		'<tr class = "" style = "" >'
		htmlstr += 			'<td colspan = "2" class= "fuente text-center" style = "border-left:2px solid black!important; border-right:2px solid black!important; border-bottom:0px!important; font-size:14px!important;"><strong>DICTAMEN</strong></td>'
		htmlstr += 		'</tr>'
		htmlstr += 		'<tr class = "" style = "" >'
		htmlstr += 			'<td width = "50%" class= "fuente text-center" style = "border-left:2px solid black!important; border-right:0px solid black!important; border-bottom:2px!important; border-top:0px!important; font-size:15px!important;" ><strong>APROBADO</strong></td>'
		htmlstr += 			'<td width = "50%" class= "fuente text-center" style = "border-left:0px solid black!important; border-right:2px solid black!important; border-bottom:2px!important; border-top:0px!important; font-size:15px!important;" ><strong>NO APROBADO</strong></td>'
		htmlstr += 		'</tr>'

	
		if dictamen:
			htmlstr += 		'<tr>'
			htmlstr += 			'<td width = "50%" class= "fuente text-center" style = "border-left:2px solid black!important; border-right:0px solid black!important; border-bottom:2px!important; border-top:0px!important; font-size:15px!important;" ><strong>X</strong></td>'
			htmlstr += 			'<td width = "50%" class= "fuente text-center" style = "border-left:0px solid black!important; border-right:2px solid black!important; border-bottom:2px!important; border-top:0px!important; font-size:15px!important;" ><strong></strong></td>'
			htmlstr += 		'</tr>'
		else:
			htmlstr += 		'<tr>'
			htmlstr += 			'<td width = "50%" class= "fuente text-center" style = "border-left:2px solid black!important; border-right:0px solid black!important; border-bottom:2px!important; border-top:0px!important; font-size:15px!important;" ><strong></strong></td>'
			htmlstr += 			'<td width = "50%" class= "fuente text-center" style = "border-left:0px solid black!important; border-right:2px solid black!important; border-bottom:2px!important; border-top:0px!important; font-size:15px!important;" ><strong>X</strong></td>'
			htmlstr += 		'</tr>'


		htmlstr += '</table>'
		htmlstr += '<table  width = "100%" style = "" >'
		htmlstr += 		'<tr class = "no_border" >'
		htmlstr += 			'<td colspan = "4" class= "fuente" ><strong>RECOMENDACIONES DETALLADAS:</strong><br>'+recomendaciones+'</strong></td>'
		htmlstr += 		'</tr>'
		htmlstr += '</table>'
		htmlstr += '<table  width = "100%" style = "" >'
		htmlstr += 		'<tr>'
		htmlstr += 			'<td width = "30%" style = "border-bottom:1px solid black!important; border-top:0px solid black!important; border-left:2px solid black!important; border-right:0px solid black!important;font-size:11px;" >'
		htmlstr += 				'&nbsp;&nbsp;NOMBRE Y FIRMA DE SINODAL:'
		htmlstr += 			'</td>'
		htmlstr += 			'<td width = "70%" style = "border-bottom:1px solid black!important; border-top:0px solid black!important; border-left:1px solid black!important; border-right:2px solid black!important;font-size:11px;" >'+nombre_sinodal+'</td>'
		htmlstr += 		'</tr>'
		htmlstr += 		'<tr>'
		htmlstr += 			'<td width = "30%" style = "border-bottom:1px solid black!important; border-top:0px solid black!important; border-left:2px solid black!important; border-right:0px solid black!important;font-size:11px;" >'
		htmlstr += 				'&nbsp;&nbsp;ACADEMIA:'
		htmlstr += 			'</td>'
		htmlstr += 			'<td width = "70%" style = "border-bottom:1px solid black!important; border-top:0px solid black!important; border-left:1px solid black!important; border-right:2px solid black!important;font-size:11px;" >'+academia+'</td>'
		htmlstr += 		'</tr>'
		htmlstr += 		'<tr>'
		htmlstr += 			'<td width = "30%" style = "border-bottom:1px solid black!important; border-top:0px solid black!important; border-left:2px solid black!important; border-right:0px solid black!important;font-size:11px;" >'
		htmlstr += 				'&nbsp;&nbsp;DEPARTAMENTO:'
		htmlstr += 			'</td>'
		htmlstr += 			'<td width = "70%" style = "border-bottom:1px solid black!important; border-top:0px solid black!important; border-left:1px solid black!important; border-right:2px solid black!important;font-size:11px;" >'+departamento+'</td>'
		htmlstr += 		'</tr>'
		htmlstr += 		'<tr>'
		htmlstr += 			'<td width = "30%" style = "border-bottom:2px solid black!important; border-top:0px solid black!important; border-left:2px solid black!important; border-right:0px solid black!important;font-size:11px;" >'
		htmlstr += 				'&nbsp;&nbsp;CONTACTO:'
		htmlstr += 			'</td>'
		htmlstr += 			'<td width = "70%" style = "border-bottom:2px solid black!important; border-top:0px solid black!important; border-left:1px solid black!important; border-right:2px solid black!important;font-size:11px;" ><a href="mailto:'+contacto+'">'+contacto+'</a></td>'
		htmlstr += 		'</tr>'
		htmlstr += '</table>'
		htmlstr += '</div>'
		htmlstr += '<div class="row">'
		htmlstr += '<div class="col-12 d-flex justify-content-center" style = "margin-top:35px;">'
		htmlstr +=		'<img src="data:image/png;base64,'+data_footer+'" width = "950" height = "163">'
		htmlstr += '</div>'
		htmlstr += '</div>'
		htmlstr += '</body>'
		htmlstr += '</html>'
		pdfkit.from_string(htmlstr, dir_pdf)

		document = open(dir_pdf, 'rb')
		response = HttpResponse(FileWrapper(document), content_type='application/msword')
		response['Content-Disposition'] = 'attachment'
		return response		
		


