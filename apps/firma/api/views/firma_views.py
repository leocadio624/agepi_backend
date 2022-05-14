import os
from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.firma.models import Firma
from apps.comunidad.models import Alumno, Profesor

from apps.firma.api.serializers.firma_serializers import FirmaSerializer
from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.protocol.api.serializers.protocol_serializers import ProtocolSerializer


from django.utils import timezone
from datetime import date

from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pathlib import Path

#firma electronica
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import base64

from django.http import HttpResponse
from wsgiref.util import FileWrapper

import string
import random


class FirmaViewSet(viewsets.ModelViewSet):
    serializer_class    = FirmaSerializer
        
    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(fk_user = pk).order_by('-created_date')
        
    #get
    def list(self, request):
        pk_user = request.GET["pk_user"]
        serializer = self.get_serializer(self.get_queryset(pk_user), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def getNameFirma(self, rol, pk, name, last_name):
        if  rol == 1:
            boleta = Alumno.objects.filter(fk_user = pk, state = True).first().boleta
            return name + '_' + last_name + '_' + boleta

        else:
            noEmpleado = Alumno.objects.filter(fk_user = pk, state = True).first().noEmpleado
            return name + '_' + last_name + '_' + noEmpleado

    #post
    def create(self, request):

        fk_user     = request.data['fk_user']
        rol_user    = request.data['rol_user']
        name        = request.data['name']
        last_name   = request.data['last_name']
        password    = request.data['password']
        vigencia    = int(request.data['vigencia'])

        

        firma = self.get_serializer().Meta.model.objects.filter(fk_user = fk_user, state = True).first()
        if firma:
            return Response({'message':'Ya cuentas con una firma electronica'}, status = status.HTTP_226_IM_USED)


        date1 = date.today()
        date2 = date(date1.year + vigencia, date1.month, date1.day)
        delta = str( (date2-date1).days )

        
        os.system('mkdir -p firmas/' + str(fk_user)+ '')
        nombre = self.getNameFirma(rol_user, fk_user, name, last_name);
        public = nombre + '.cer'
        private = nombre + '.key'


        path_public     = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/' + public
        public_pem     = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/public.pem'

        path_private    = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/' + private
        private_pem    = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/private.pem'

        ruta_firma      = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/'


        

        
        cadena = 'openssl req -x509 -inform der -sha1 -days '+delta+' -newkey rsa:2048 -passout pass:'+password+''
        cadena += ' -subj "/C=MX/ST=CIUDAD DE MEXICO/L=GAM/O=AGEPI/OU=IT Department AGEPI/CN=AUTORIDAD NO CERTIFICADORA"'
        cadena += ' -inform der -keyout '+path_private+' -out '+path_public+''

        
        os.system(cadena)        

        os.system('openssl x509 -in '+path_public+' -out '+public_pem)
        os.system('openssl pkcs8 -in '+path_private+' -out '+private_pem+' -passin pass:'+password+'')

        
    
        try:
            f = open(path_public, "r")
        except:
            return Response({'message':'Ocurrio un error en la generacion del certificado de tú firma electronica'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            f = open(path_private, "r")
        except:
            return Response({'message':'Ocurrio un error en la generacion de la llave privada de tú firma electronica'}, status = status.HTTP_400_BAD_REQUEST)
        

        serializer = self.serializer_class(data =
                                            {   
                                            'fk_user'           :fk_user,
                                            'password_firma'    :password,
                                            'ruta_public_key'   :path_public,
                                            'ruta_private_key'  :path_private,
                                            'ruta_firma'        :ruta_firma,
                                            'vigencia_firma'    :date2})
        if  serializer.is_valid():
            serializer.save()
            return Response({'message':'Se ha generado tu firma electronica correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'Ocurrio un error en la generacion de tú firma electronica'}, status = status.HTTP_400_BAD_REQUEST)


    def get_querySetInstance(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    

    def destroy(self, request, pk = None):
        firma = self.get_serializer().Meta.model.objects.filter(id = pk).first()
        
        ruta_public_key = request.data['ruta_public_key']
        ruta_private_key = request.data['ruta_private_key']

        #ruta de donde se guardan los archivos
        #dir_name = os.path.dirname(request.data['ruta_public_key'])
            
        if  firma:
            firma.state = False
            firma.save()
            os.system('rm ' +ruta_public_key+'')
            os.system('rm ' +ruta_private_key+'')

            return Response({'message':'Se ha cancelado tú firma electrónica'}, status = status.HTTP_200_OK)
        return Response({'message':'Ocurrió un error en la cancelacion de tú firma electrónica'}, status = status.HTTP_400_BAD_REQUEST)

class FirmaPassViewSet(viewsets.ModelViewSet):
    serializer_class    = FirmaSerializer

    

    #post
    def create(self, request):
        pk_firma = request.data['pk_firma']
        firma = self.get_serializer().Meta.model.objects.filter(id = pk_firma, state = True).first()

        if  firma:
            try:
                self.sendEmailPass(firma.fk_user.name, firma.fk_user.last_name, firma.fk_user.email, firma.password_firma)
                return Response({'message':'Contraseña enviada'}, status = status.HTTP_200_OK)
            except:
                return Response({'message':'Ocurrió un error en el envio de tú contraseña'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Ocurrió un error en el envio de tú contraseña'}, status = status.HTTP_400_BAD_REQUEST)


    def sendEmailPass(self, name, last_name, receiver, passFirma):

        receiver = 'leocadio624@gmail.com'
        host = settings.EMAIL_HOST
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Contraseña de firma electrónica'
        email_body = 'Hola '+name+' '+last_name+' tu contraseña de firma electrónica vigente es: '+str(passFirma)+''


        msg.attach(MIMEText(email_body, 'plain'))
        email_body_content = msg.as_string()

        server = smtplib.SMTP(host)
        server.starttls()

        server.login(sender, password)
        server.sendmail(sender, receiver, email_body_content)
        server.quit()


class FirmaDownloadViewSet(viewsets.ModelViewSet):

    #post
    def create(self, request):

        try:
            path = request.data['ruta_archivo']
            document = open(path, 'rb')
            response = HttpResponse(FileWrapper(document))
            response['Content-Disposition'] = 'attachment'
            return response
        except:
            return Response({'message':'Ocurrió un error en la descarga del archivo'}, status = status.HTTP_400_BAD_REQUEST)



"""
* Descripcion: Carga catalogo al iniciar modulo
* verifica firmas
* Fecha de la creacion:     12/05/2022
* Author:                   Eduardo B 
"""
class verificaFirmaStartViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer
    def get_queryset(self, pk = None):

        equipos = self.get_serializer().Meta.model.objects.filter(fk_user = pk, solicitudEquipo = 2, state = True).values('fk_team')
        protocolos = ProtocolSerializer.Meta.model.objects.filter(fk_team__in = equipos, state = True)
        return protocolos

    #get
    def list(self, request):
        pk_user = request.GET["pk_user"]
        protocolos = ProtocolSerializer(self.get_queryset(pk_user), many = True)
        return Response(protocolos.data, status = status.HTTP_200_OK)


"""
* Descripcion: Dado un pk de protocolo, devuelve
* los integrantes del protocolo
* verifica firmas
* Fecha de la creacion:     14/05/2022
* Author:                   Eduardo B 
"""
class getIntegrantesProtocoloViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer
    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(fk_team = pk, solicitudEquipo = 2, state = True)

    #get
    def list(self, request):
        pk_protocol = request.GET["pk_protocol"]
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id = pk_protocol, state = True).first()
        if  protocolo is None:
            return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        fk_team = protocolo.fk_team.id
        integrantes = self.serializer_class(self.get_queryset(fk_team), many = True)

        return Response(integrantes.data, status = status.HTTP_200_OK)


"""
* Descripcion: Verifica una firma dado el sello digital
* Fecha de la creacion:     12/05/2022
* Author:                   Eduardo B 
"""
class verificaFirmaViewSet(viewsets.ModelViewSet):
    serializer_class = ProtocolSerializer
    
    def create(self, request):

        pk_protocol  = request.data['pk_protocol']
        pk_user   = request.data['pk_user']
        firma   = request.data['firma']

        base         = Path(__file__).resolve().parent.parent.parent.parent.parent
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id = pk_protocol, state = True).first()
        if  protocolo is None:
            return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)
        protocolo_serializer    = ProtocolSerializer(ProtocolSerializer.Meta.model.objects.filter(id = pk_protocol, state = True).first(), many = False)
        
        firmaObj = FirmaSerializer.Meta.model.objects.filter(fk_user = pk_user, state = True).first()
        if  firmaObj is None:
            return Response({'message':'Este miembro de equipo aun no ha firmado el protocolo'}, status = status.HTTP_400_BAD_REQUEST)


        fileProtocol = protocolo_serializer.data['fileProtocol']
        pathFile    = str(base) + str(fileProtocol)
        public_key   = firmaObj.ruta_public_key

        
        try:
            firma = firma.encode('UTF-8')
            firma = base64.b64decode(firma)
        except:
            return Response({'message':'La firma proporcionada no es válida en el protocolo'}, status = status.HTTP_400_BAD_REQUEST)


        f = open(public_key, 'r')
        pubKey = RSA.import_key(f.read())
        f.close()

        archivo = open(pathFile, 'rb').read()
        hash = SHA256.new(archivo)
        verifier = PKCS115_SigScheme(pubKey)

        try:
            verifier.verify(hash, firma)
            return Response({'message':'La firma es válida en el protocolo'}, status = status.HTTP_200_OK)
        except:
            return Response({'message':'La firma proporcionada no es válida en el protocolo'}, status = status.HTTP_400_BAD_REQUEST)
            


        
