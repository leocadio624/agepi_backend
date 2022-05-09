from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.notification.api.serializers.notificacion_serializers import NotificacionTeamSerializer, SolicitudFirmaSerializer
from apps.firma.api.serializers.firma_serializers import FirmaProtocoloSerializer

from apps.protocol.api.serializers.protocol_serializers import ProtocolSerializer
from apps.protocol.models import ProtocolState
from apps.team.models import TeamMembers
from apps.firma.models import Firma


from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse
from wsgiref.util import FileWrapper

#almacenar archivo
import os
from pathlib import Path
from django.core.files.storage import FileSystemStorage

#firma electronica
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
import base64
"""
"""



"""
* Descripcion: Inicialializa modulo Solicitudes firma
* Fecha de la creacion:     06/05/2022
* Author:                   Eduardo B 
"""
class SolicitudesFirmaViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitudFirmaSerializer

    def get_queryset(self, pk = None):
        objects = TeamMembers.objects.filter(state = True, fk_user = pk).values('id')
        return self.get_serializer().Meta.model.objects.filter(fk_tipoNotificacion = 4, fk_userDestino__in = objects).order_by('-created_date')

    #get
    def list(self, request):
        pk_user = request.GET["pk_user"]
        serializer = self.get_serializer(self.get_queryset(pk_user), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class existeFirmaViewSet(viewsets.ModelViewSet):
    serializer_class = FirmaProtocoloSerializer

    def create(self, request):

        pk_user = request.data['pk_user']
        pk_protocol  = request.data['pk_protocol']


        firmas_protocolo = FirmaProtocoloSerializer.Meta.model.objects.filter(fk_protocol = pk_protocol, fk_user = pk_user, state = True).first()
        if  firmas_protocolo:
            return Response({'message':'Ya haz firmado este protocolo'}, status = status.HTTP_226_IM_USED)

        firmas = Firma.objects.filter(fk_user = pk_user, state = True).first()

        if  firmas is None:
            return Response({'message':'sin firma registrada'}, status = status.HTTP_206_PARTIAL_CONTENT)
        return Response({'message':'continua'}, status = status.HTTP_200_OK)


class firmaDocumentoViewSet(viewsets.ModelViewSet):
    serializer_class = FirmaProtocoloSerializer

    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    #get
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        
        pk_user         = request.data['pk_user']
        pk_protocol     = request.data['pk_protocol']
        fileProtocol    = request.data['fileProtocol']
        private         = request.FILES.get("private_key")
        password        = request.data['password']

        firma = Firma.objects.filter(fk_user = pk_user, state = True).first()
        if  firma is None:
            return Response({'message':'Ocurrió una interrupcción en la comprobación de tu firma electronica, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        ruta_firma      = firma.ruta_firma
        base            = Path(__file__).resolve().parent.parent.parent.parent.parent
        pathFile        = str(base) + str(fileProtocol)
        dir_protocol    = os.path.dirname(pathFile) +'/'+str(pk_user)+'/'

        
        os.system('rm '+dir_protocol+'*')
        fss         = FileSystemStorage(location = dir_protocol)
        llave       = fss.save(private.name, private)


        in_key  = dir_protocol + private.name + ''
        out_key = dir_protocol + 'private.pem'


        os.system('openssl pkcs8 -in '+in_key+' -out '+out_key+' -passin pass:'+password+'')
        f = open(out_key, "r")
        f.close()

        
        try:
            f = open(out_key, 'r')
            keyPair = RSA.import_key(f.read())
        except:
            return Response({'message':'Contraseña de firma electrónica incorrecta, favor de verificarlo'}, status = status.HTTP_400_BAD_REQUEST)

        archivo = open(pathFile, 'rb').read()
        f.close()
        hash = SHA256.new(archivo)
        
        signer = PKCS115_SigScheme(keyPair)
        signature = signer.sign(hash)

        firma = base64.b64encode(signature)
        firma = firma.decode('UTF-8')

        #signature2 = signature.encode()
        #signature2 = base64.b64decode(signature2)
        
        f = open(ruta_firma+'public.pem', 'r')
        pubKey = RSA.import_key(f.read())
        f.close()
        verifier = PKCS115_SigScheme(pubKey)


        try:

            verifier.verify(hash, signature)
            serializer = self.serializer_class(data = {
                        'fk_protocol':pk_protocol,
                        'fk_user':pk_user,
                        'firma':firma
                        })

            if  serializer.is_valid():
                serializer.save()
                return Response({'message':'Se ha firmado el protocolo correctamente'}, status = status.HTTP_200_OK)
            return Response({'message':'Ocurrio una interrupcción, favor de intentarlo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)    

        except:
            return Response({'message':'La clave privada proporcionada no te pertenece'}, status = status.HTTP_400_BAD_REQUEST)
            
        
        
        

class FirmaProtocolosViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer


    def create(self, request):
        try:

            fk_userOrigen   = request.data['fk_userOrigen']
            fk_team         = request.data['fk_team']
            fk_protocol     = request.data['fk_protocol']

            integrantes = self.get_serializer().Meta.model.objects.filter(fk_team = fk_team, solicitudEquipo = 2, state = True)

            protocolo = ProtocolSerializer.Meta.model.objects.filter(id = fk_protocol).first()
            numero_protocolo = protocolo.number
            titulo_protocolo = protocolo.title

            fk_protocol_state = ProtocolState.objects.filter(protocol_state = 2).first()
            protocolo.fk_protocol_state = fk_protocol_state
            #protocolo.save()
            

            
            for i in integrantes:
                notificacion_serilizer   = NotificacionTeamSerializer(data = {'fk_userOrigen':fk_userOrigen, 'fk_userDestino':i.id, 'fk_tipoNotificacion':4})
                if  notificacion_serilizer.is_valid():
                    #notificacion_serilizer.save()
                    self.sendEmailPass(i.fk_user.name, i.fk_user.last_name, i.fk_user.email, numero_protocolo, titulo_protocolo)

            return Response({'message':'Se han enviado las solicitudes de firma a los integrantes de equipo'}, status = status.HTTP_200_OK)
        except:
            return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)
        

    def sendEmailPass(self, name, last_name, receiver, numero, titulo):

        receiver = 'leocadio624@gmail.com'
        host = settings.EMAIL_HOST
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Solicitud firma protocolo'
        email_body = 'Hola '+name+' '+last_name+' tienes el protocolo con número: '+numero+' y título \"'+titulo+'\" pendiente por firmar.'


        msg.attach(MIMEText(email_body, 'plain'))
        email_body_content = msg.as_string()

        server = smtplib.SMTP(host)
        server.starttls()

        server.login(sender, password)
        server.sendmail(sender, receiver, email_body_content)
        server.quit()


            
        
        