import pytz
from django.utils import timezone
from datetime import date

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.protocol.api.serializers.protocol_serializers import (ProtocolSerializer, AsignacionProtocoloSerializer,
                                                                SelectProtocoloSerializer, SelectProtocoloLineSerializer, EvaluacionSerializer, PreguntaSerializer)
from apps.protocol.api.serializers.catalogos_serializers import PeriodoListSerializer, ProtocolStateSerializer, AcademiaSerializer
from apps.team.api.serializers.team_serializers import TeamMemberDictamenSerializer, AlumnoTeamSerializer, TeamMemberSerializer




import os
import pdfkit
import base64

from pathlib import Path
from django.http import HttpResponse
from wsgiref.util import FileWrapper

#Correos
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse
from wsgiref.util import FileWrapper





class ProtocolCattStartViewSet(viewsets.ModelViewSet):
    serializer_class = ProtocolSerializer

    def get_estados(self, pk = None):
        return ProtocolStateSerializer.Meta.model.objects.all()

    def get_periodo(self, pk = None):
        #return PeriodoListSerializer.Meta.model.objects.filter(state = True)
        return PeriodoListSerializer.Meta.model.objects.all()

    def get_academias(self, pk = None):
        return AcademiaSerializer.Meta.model.objects.all()

    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(state = True)
    
    #get
    def list(self, request):        
        periodo_serializer = PeriodoListSerializer(self.get_periodo(), many = True)
        estados_serializer = ProtocolStateSerializer(self.get_estados(), many = True)
        academias_serializer = AcademiaSerializer(self.get_academias(), many = True)
        protocol_serializer = self.get_serializer(self.get_queryset(), many = True)

        
        return Response({
            'periodos':periodo_serializer.data,
            'estados':estados_serializer.data,
            'academias':academias_serializer.data,
            'protocolos':protocol_serializer.data
        },status = status.HTTP_200_OK)

        


class filtrarProtocolosViewSet(viewsets.ModelViewSet):
    serializer_class = ProtocolSerializer

    def get_protocols(self, periodo, estado):

        if(periodo == -1 and estado == -1):
            return self.get_serializer().Meta.model.objects.filter(state = True)

        elif(periodo == -1 and estado != -1):
            return self.get_serializer().Meta.model.objects.filter(fk_protocol_state = estado, state = True)

        elif(periodo != -1 and estado == -1):
            return self.get_serializer().Meta.model.objects.filter(fk_periodo = periodo, state = True)

        elif(periodo != -1 and estado != -1):
            return self.get_serializer().Meta.model.objects.filter(fk_protocol_state = estado, fk_periodo = periodo, state = True)
    


    def create(self, request):

        periodo = request.data['periodo']
        estado = request.data['estado']

        protocol_serializer = self.get_serializer(self.get_protocols(periodo, estado), many = True)

        return Response(protocol_serializer.data, status = status.HTTP_200_OK)


class asignacionProtocoloViewSet(viewsets.ModelViewSet):
    serializer_class = AsignacionProtocoloSerializer

    def create(self, request):
        
        fk_protocol = request.data['pk_protocol']
        academias = request.data['academias']

        try:
            for i in academias:
                asigacion_serializer = self.serializer_class(data = {'fk_protocol':fk_protocol, 'fk_academia':i})
                if  asigacion_serializer.is_valid():
                    asigacion_serializer.save()
                    

            protocolo = ProtocolSerializer.Meta.model.objects.filter(id = fk_protocol).first()
            fk_protocol_state = ProtocolStateSerializer.Meta.model.objects.filter(protocol_state = 4).first()
            protocolo.fk_protocol_state = fk_protocol_state
            protocolo.save()

            return Response({'message':'Se ha asignado el protocolo correctamente'},status = status.HTTP_200_OK)

        except:
            return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

class asignacionAcademiasViewSet(viewsets.ModelViewSet):
    serializer_class = AsignacionProtocoloSerializer

    def create(self, request):
        protocolos = request.data['protocolos']
        
        for i in protocolos:

            protocolo = ProtocolSerializer.Meta.model.objects.filter(id = i).first()
            fk_protocol_state = ProtocolStateSerializer.Meta.model.objects.filter(protocol_state = 5).first()
            protocolo.fk_protocol_state = fk_protocol_state
            protocolo.save()


        return Response({'message':'Se han enviado los protocolos a las academias'},status = status.HTTP_200_OK)

"""
* Descripcion: Linea protocolos paso 4
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class getFechaAsignacionViewSet(viewsets.ModelViewSet):
    serializer_class = AsignacionProtocoloSerializer

    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%m/%d/%Y %H:%M:%S')

    def create(self, request):
        
        fk_protocol = request.data['fk_protocol']
        asignacion  = self.serializer_class().Meta.model.objects.filter(fk_protocol = fk_protocol, state = True).first()

        fecha_asignacion = asignacion.created_date
        fecha_asignacion = self.convertUTC(fecha_asignacion)
    
        return Response({'fecha_asignacion':fecha_asignacion},status = status.HTTP_200_OK)

"""
* Descripcion: Linea protocolos paso 5
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class getProfesoresSeleccionViewSet(viewsets.ModelViewSet):
    serializer_class = SelectProtocoloLineSerializer

    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%m/%d/%Y %H:%M:%S')


    def get_queryset(self, pk = None):
        return self.serializer_class().Meta.model.objects.filter(fk_protocol = pk, state = True).order_by('created_date')

    def create(self, request):
        fk_protocol = request.data['fk_protocol']
        serializador = self.serializer_class(self.get_queryset(fk_protocol), many = True)

        return Response(serializador.data,status = status.HTTP_200_OK)

        

"""
* Descripcion: Linea protocolos paso 6
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class getFechaEvaluacionViewSet(viewsets.ModelViewSet):
    

    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%d/%m/%Y %H:%M:%S')

    def create(self, request):

        fk_protocol = request.data['fk_protocol']
        select_protocol = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True).values('id')

        evaluaciones = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion__in = select_protocol, state = True).values('created_date').order_by('-created_date')

        fecha_evaluacion = evaluaciones[0]['created_date']
        fecha_evaluacion = self.convertUTC(fecha_evaluacion)

        
        return Response({'fecha_evaluacion':fecha_evaluacion},status = status.HTTP_200_OK)

"""
* Descripcion: Obtiene la fecha del dictamen
* Fecha de la creacion:     01/06/2022
* Author:                   Eduardo Bernal Leocadio
"""
class getFechaDictamenViewSet(viewsets.ModelViewSet):
    
    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%d/%m/%Y %H:%M:%S')

    def create(self, request):
        fk_protocol = request.data['fk_protocol']
        protocol = ProtocolSerializer.Meta.model.objects.filter(id = fk_protocol, state = True).first()
        fecha_dictamen = self.convertUTC(protocol.modified_date)
        
        return Response({'fecha_dictamen':fecha_dictamen},status = status.HTTP_200_OK)



class selectProtocolViewSet(viewsets.ModelViewSet):
    serializer_class = SelectProtocoloSerializer

    def create(self, request):
        fk_protocol = request.data['fk_protocol']
        fk_user     = request.data['fk_user']

        serializer = self.serializer_class(data = {'fk_protocol':fk_protocol, 'fk_user':fk_user})
        if  serializer.is_valid():
            serializer.save()

    
            select = self.serializer_class().Meta.model.objects.filter(fk_protocol = fk_protocol, state = True)
            if  len(select) == 3:
                fk_protocol_state = ProtocolStateSerializer.Meta.model.objects.filter(protocol_state = 6).first()
                protocolo = ProtocolSerializer.Meta.model.objects.filter(id  = fk_protocol, state = True).first()
                protocolo.fk_protocol_state = fk_protocol_state
                protocolo.save()

                numero = protocolo.number
                titulo = protocolo.title
                fk_team = protocolo.fk_team.id


                integrantes = TeamMemberSerializer.Meta.model.objects.filter(fk_team = fk_team, state = True, solicitudEquipo = 2)
                for i in integrantes:

                    receiver = i.fk_user.email
                    receiver = 'leocadio624@gmail.com'
                    host = settings.EMAIL_HOST
                    sender = settings.EMAIL_HOST_USER
                    password = settings.EMAIL_HOST_PASSWORD
                    
                    msg = MIMEMultipart()
                    msg['From'] = sender
                    msg['To'] = receiver
                    msg['Subject'] = 'Selección protocolo'
                    email_body = 'Hola '+i.fk_user.name+' '+i.fk_user.last_name+' el protocolo con número: '+numero+' y título \"'+titulo+'\" en el que estás relacionado cambío a estado seleccionado.'
                    


                    msg.attach(MIMEText(email_body, 'plain'))
                    email_body_content = msg.as_string()

                    server = smtplib.SMTP(host)
                    server.starttls()

                    server.login(sender, password)
                    server.sendmail(sender, receiver, email_body_content)
                    server.quit()
            

                
            return Response({'message':'Se ha seleccionado el protocolo correctamente'},status = status.HTTP_200_OK)
        return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)


"""
* Descripcion: Genera evaluacion por parte de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class existeEvalucacionViewSet(viewsets.ModelViewSet):
    def create(self, request):
        fk_user     = request.data['fk_user']
        fk_protocol = request.data['fk_protocol']

        select = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol,  fk_user = fk_user, state = True).first()
        if select is None:   
            return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)
        
        fk_seleccion = select.id
        evaluacion = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion = fk_seleccion, state = True)
        if evaluacion:
            return Response({'message':'Ya haz evaluado este protocolo'}, status = status.HTTP_226_IM_USED)
        return Response({'message':1},status = status.HTTP_200_OK)

"""
* Descripcion: Genera evaluacion por parte de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class generarEvalucacionViewSet(viewsets.ModelViewSet):
    #serializer_class = SelectProtocoloSerializer

    def create(self, request):

        fk_user     = request.data['fk_user']
        name     = request.data['name']
        last_name     = request.data['last_name']
        fk_protocol = request.data['fk_protocol']
        fk_protocol_state = 0
        preguntas   = request.data['preguntas']
        summary     = request.data['summary']
        dictamen     = request.data['dictamen']
        primera_evaluacion = [1,3]
        version = 0
        
        
        protocol = ProtocolSerializer.Meta.model.objects.filter(id = fk_protocol, state = True).first()
        if protocol is None:   
            return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        numero = protocol.number
        titulo = protocol.title
        fk_team = protocol.fk_team.id
        sinodal = name + last_name

        fk_protocol_state = protocol.fk_protocol_state.id
        if protocol.fk_inscripccion.id in primera_evaluacion:
            version = 1
        else:
            version = 2
        
        
        
        select = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol,  fk_user = fk_user, state = True).first()
        fk_seleccion = select.id
        evaluacion_serializer = EvaluacionSerializer(data = {'fk_seleccion':fk_seleccion, 'observacion_general':summary, 'dictamen':dictamen, 'version':version})

        

        if  evaluacion_serializer.is_valid():
            
            evaluacion_serializer.save()
            fk_evaluacion = evaluacion_serializer.data['id']
            for i in preguntas:
                numPregunta = i['id']
                estado = i['state']
                observacion = i['summary']
            
                pregunta_serializer = PreguntaSerializer(data = {'fk_evaluacion':fk_evaluacion, 'numPregunta':numPregunta, 'estado':estado, 'observacion':observacion})
                if  pregunta_serializer.is_valid():
                    pregunta_serializer.save()




            #actualiza estado de protocolos que ya estan seleccionados '6'
            if  fk_protocol_state == 6:
                selecciones = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True).values('id')
                evaluaciones = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion__in = selecciones, state = True)

                if  len(evaluaciones) == 3:
                    fk_protocol_state = ProtocolStateSerializer.Meta.model.objects.filter(protocol_state = 7).first()
                    protocolo = ProtocolSerializer.Meta.model.objects.filter(id  = fk_protocol, state = True).first()
                    protocolo.fk_protocol_state = fk_protocol_state
                    protocolo.save()
            
            integrantes = TeamMemberSerializer.Meta.model.objects.filter(fk_team = fk_team, state = True, solicitudEquipo = 2)
            for i in integrantes:
                
                receiver = i.fk_user.email
                receiver = 'leocadio624@gmail.com'
                host = settings.EMAIL_HOST
                sender = settings.EMAIL_HOST_USER
                password = settings.EMAIL_HOST_PASSWORD
                
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = 'Evaluacion protocolo'
                email_body = 'Hola '+i.fk_user.name+' '+i.fk_user.last_name+' el protocolo con número: '+numero+' y título \"'+titulo+'\" en el que estás relacionado ha sido evaluado por el sinodal '+sinodal+'.'
                


                msg.attach(MIMEText(email_body, 'plain'))
                email_body_content = msg.as_string()

                server = smtplib.SMTP(host)
                server.starttls()

                server.login(sender, password)
                server.sendmail(sender, receiver, email_body_content)
                server.quit()
            


            return Response({'message':'Se ha generado la evaluación correctamente'},status = status.HTTP_200_OK)
        return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        
"""
* Descripcion: Genera tabla con evaluacion de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
"""
class getFechaEvaluacionViewSet(viewsets.ModelViewSet):
    serializer_class = SelectProtocoloLineSerializer

    def get_queryset(self, pk = None):
        return self.serializer_class().Meta.model.objects.filter(fk_protocol = pk, state = True).order_by('created_date')

    def create(self, request):
        fk_protocol = request.data['fk_protocol']
        serializador = self.serializer_class(self.get_queryset(fk_protocol), many = True)

        last = len(serializador.data) - 1
        fecha_evaluacion = serializador.data[last]['fecha_evaluacion']
        
        return Response({'fecha_evaluacion':fecha_evaluacion},status = status.HTTP_200_OK)
"""


"""
* Descripcion: Genera tabla con evaluacion de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class generarDictamenViewSet(viewsets.ModelViewSet):



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

    def getAlumnos(self, fk_team):
        alumnos = AlumnoTeamSerializer.Meta.model.objects.filter(alta_app = True, state = True).values('fk_user')
        integrantes = TeamMemberDictamenSerializer(TeamMemberDictamenSerializer.Meta.model.objects.filter(fk_team = fk_team, fk_user__in = alumnos, solicitudEquipo = 2, state = True), many = True)
        return integrantes.data

    def getSinodales(self, fk_protocol):

        sinodales = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True)
        arr_sinodales = []

        for i in sinodales:arr_sinodales.append(i.fk_user.name+' '+i.fk_user.last_name)
        return arr_sinodales
        

    def create(self, request):

        fk_protocol = request.data['fk_protocol']
        protocol_serializer = ProtocolSerializer(ProtocolSerializer.Meta.model.objects.filter(id=fk_protocol).first(), many = False)
        fileProtocol = protocol_serializer.data['fileProtocol']

        base            = Path(__file__).resolve().parent.parent.parent.parent.parent
        pathFile        = str(base) + str(fileProtocol)
        dir_pdf         = os.path.dirname(os.path.realpath(pathFile)) + '/dictamen.pdf'

        
        select = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True).values('id')
        evaluaciones = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion__in = select, state = True)

        dictamen = True
        for i in evaluaciones:
            if i.dictamen == False : dictamen = False


        


        fk_protocol_state = ProtocolStateSerializer.Meta.model.objects.filter(protocol_state = 8).first()
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id  = fk_protocol, state = True).first()
        protocolo.dictamen = dictamen
        protocolo.fk_protocol_state = fk_protocol_state

        titulo = protocolo.title
        numero = protocolo.number
        periodo = protocolo.fk_periodo.periodo
        anio = protocolo.fk_periodo.anio
        dictamen = protocolo.dictamen

        #protocolo.save()

        cadena_periodo  = ""
        cadena_dictamen = ""
        cadena_dictamen = "APROBADO" if dictamen else "NO APROBADO"

        if periodo == 1:
            cadena_periodo = str(anio)+'-2 / '+str(anio+1)+'-1'
        elif periodo ==2:
            cadena_periodo = str(anio+1)+'-1 / '+str(anio+1)+'-2'


        fk_team = protocolo.fk_team.id
        alumnos = self.getAlumnos(fk_team)
        sinodales = self.getSinodales(fk_protocol)

        #return Response({'message':'Se ha generado el dictamen de protocolo correctamente'},status = status.HTTP_200_OK)


        fecha   = date.today()
        dia     = fecha.day
        mes     = fecha.month
        anio    = fecha.year


        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        fecha_dictamen = 'CDMX, a ' + str(dia)+' de '+meses[mes-1]+' del '+str(anio)
        
        """
        Obtiene el nombre del dia de la fecha
        print(protocolo.modified_date.strftime("%A"))
        """

        logo_ipn        = str(base) + '/logo-ipn.png'
        logo_escom      = str(base) + '/escom.png'
        firma_dictamen  = str(base) + '/firma_dictamen.png'

        data_ipn    = self.get_image_file_as_base64_data(logo_ipn)
        data_escom  = self.get_image_file_as_base64_data(logo_escom)
        data_firma  = self.get_image_file_as_base64_data(firma_dictamen)

        

        htmlstr = '<!doctype html>'
        htmlstr +='<html lang="en">'
        htmlstr +='<head>'
        htmlstr +='<meta charset="utf-8">'
        htmlstr +='<meta name="viewport" content="width=device-width, initial-scale=1">'
        htmlstr +='<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">'
        htmlstr +='</head>'

        htmlstr += '<style>'
        htmlstr += '.header_1{'
        htmlstr +=    'font-size:24px;'
        htmlstr +=    'font-family: "Courier Rough Bold";'
        htmlstr += '}'
        htmlstr += '.header_2{'
        htmlstr +=    'font-size:20px;'
        htmlstr +=    'font-family: "Courier Rough Bold";'
        htmlstr += '}'
        htmlstr += '.header_3{'
        htmlstr +=    'font-size:16px;'
        htmlstr +=    'font-family: "Times New Roman", serif;'
        htmlstr += '}'
        htmlstr += '.header_4{'
        htmlstr +=    'font-size:15px;'
        htmlstr +=    'font-family: "Times New Roman", serif;'
        htmlstr += '}'
        htmlstr += '.fuente{'
        htmlstr +=    'font-size:17px;'
        htmlstr +=    'text-align:justify;'
        htmlstr +=    'padding-top:5px;'
        htmlstr +=    'padding-bottom:5px;'
        htmlstr += '}'



        htmlstr += '.container{'
        htmlstr += 'margin-left: 30px!important;'
        htmlstr += 'margin-right: 30px!important;'
        htmlstr += 'max-width: 950px!important;'
        htmlstr += '}'
        htmlstr += '</style>'


        htmlstr +='<body>'
        htmlstr +='<br>'
        htmlstr +='<div class= "row" >'
        htmlstr +=      '<div class = "col-3 d-flex justify-content-start">'
        htmlstr +=          '<img width = "170" height = "120" src="data:image/png;base64,'+data_ipn+'">'
        htmlstr +=      '</div>'
        htmlstr +=      '<div class = "col-6 d-flex justify-content-center">'
        htmlstr +=          '<table class = "row">'
        htmlstr +=              '<tr><td class = "header_1 text-center">INSTITUTO POLIT&Eacute;CNICO NACIONAL</td></tr>'
        htmlstr +=              '<tr><td class = "header_2 text-center">ESCUELA SUPERIOR DE C&Oacute;MPUTO</td></tr>'
        htmlstr +=              '<tr><td class = "header_3 text-center">SUBDIRECCI&Oacute;N ACAD&Eacute;MICA</td></tr>'
        htmlstr +=              '<tr><td class = "header_4 text-center">Departamento de Formaci&oacute;n Integral e Intitucional</td></tr>'
        htmlstr +=              '<tr><td class = "header_4 text-center">Comisi&oacute;n Acad&eacute;mica de Trabajos Terminales</td></tr>'
        htmlstr +=          '</table>'
        htmlstr +=      '</div>'
        htmlstr +=      '<div class = "col-3 d-flex justify-content-end">'
        htmlstr +=          '<img width = "170" height = "120" src="data:image/png;base64,'+data_escom+'">'
        htmlstr +=      '</div>'
        htmlstr +='</div>'
        htmlstr +='<br>'
        htmlstr +='<div class= "row container" >'
        htmlstr +=      '<div class = "col-12 d-flex justify-content-end">'
        htmlstr +=              '<div class = "header_4 text-center">'+fecha_dictamen+'</div>'
        htmlstr +=      '</div>'
        htmlstr +='</div>'
        htmlstr +='<div class= "row container" >'
        htmlstr +=      '<div class = "col-12 d-flex justify-content-end">'
        htmlstr +=              '<div class = "header_4 text-center">DFII/CATT/DICT/'+str(anio)+'</div>'
        htmlstr +=      '</div>'
        htmlstr +='</div>'
        alumnos
        for i in alumnos:
            htmlstr +='<div class= "row container" >'
            htmlstr +=      '<div class = "col-12 d-flex justify-content-start">'
            htmlstr +=          '<div class = "fuente"><strong>C. '+i['last_name']+' '+i['name']+'</strong></div>'
            htmlstr +=      '</div>'
            htmlstr +='</div>'
        htmlstr +='<div class= "row container" >'
        htmlstr +=      '<div class = "col-12 d-flex justify-content-start">'
        htmlstr +=          '<div class = "fuente"><strong>PRESENTES</strong></div>'
        htmlstr +=      '</div>'
        htmlstr +='</div>'

        cadena = 'Con base en los lineamientos en el Documento Rector de Trabajos Terminales, se comunica que la propuesta de Trabajo Terminal: <strong><i>"'+titulo+'"</i></strong>,'
        cadena += ' con n&uacute;mero de registro <strong><i>'+numero+'</i></strong>, ha sido dictaminada <strong><u>'+cadena_dictamen+'</u></strong>, para realizarse en el ciclo escolar'
        cadena += ' <strong>'+cadena_periodo+'</strong>.'


        htmlstr +='<div class= "row container" >'
        htmlstr +=      '<div class = "col-12 d-flex justify-content-start">'
        htmlstr +=          '<div class = "fuente">'+cadena+'</div>'
        htmlstr +=      '</div>'
        htmlstr +='</div>'
        htmlstr +='<div class= "row container" >'
        htmlstr +=      '<div class = "col-12 d-flex justify-content-start">'
        htmlstr +=          '<div class = "fuente" >Por &uacute;ltimo, se le(s) informa que los profesores sinodales en este protocolo son:</div>'
        htmlstr +=      '</div>'
        htmlstr +='</div>'

        for i in sinodales:
            htmlstr +='<div class= "row container" >'
            htmlstr +=      '<div class = "col-12 d-flex justify-content-start">'
            htmlstr +=          '<div class = "fuente" >'+i+'</div>'
            htmlstr +=      '</div>'
            htmlstr +='</div>'


       

        htmlstr +='<div class= "row container" style = "margin-top:40px">'
        htmlstr +=      '<div class = "col-12 d-flex justify-content-start">'
        htmlstr +=          '<div class = "fuente" >Sin otro particular, se envia un cordial saludo.</div>'
        htmlstr +=      '</div>'
        htmlstr +='</div>'
        htmlstr +='<div class= "row container" >'
        htmlstr +=      '<div class = "col-3 d-flex justify-content-start">'
        htmlstr +=          '<img width = "320" height = "270" src="data:image/png;base64,'+data_firma+'">'
        htmlstr +=      '</div>'
        htmlstr +='</div>'
        htmlstr +='</body>'
        htmlstr +='</html>'
        pdfkit.from_string(htmlstr, dir_pdf)    
        return Response({'message':'Se ha generado el dictamen de protocolo correctamente'},status = status.HTTP_200_OK)


"""
* Descripcion: Genera tabla con evaluacion de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class verDictamenViewSet(viewsets.ModelViewSet):

    def create(self, request):

        fk_protocol = request.data['fk_protocol']
        protocol_serializer = ProtocolSerializer(ProtocolSerializer.Meta.model.objects.filter(id=fk_protocol).first(), many = False)
        fileProtocol = protocol_serializer.data['fileProtocol']

        base            = Path(__file__).resolve().parent.parent.parent.parent.parent
        pathFile        = str(base) + str(fileProtocol)
        dir_pdf         = os.path.dirname(os.path.realpath(pathFile)) + '/dictamen.pdf'

        document = open(dir_pdf, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment'
        return response

        """
        print(dir_pdf)
        return Response({'message':'mensaje generico'},status = status.HTTP_200_OK)
        """
