from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.notification.api.serializers.notificacion_serializers import NotificacionTeamSerializer, SolicitudFirmaSerializer

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
    def create(self, request):
        pk_user = request.data['pk_user']
        firmas = Firma.objects.filter(fk_user = pk_user, state = True).first()
        if  firmas is None:
            return Response({'message':'sin firma registrada'}, status = status.HTTP_206_PARTIAL_CONTENT)
        return Response({'message':'continua'}, status = status.HTTP_200_OK)

class firmaDocumentoViewSet(viewsets.ModelViewSet):
    def create(self, request):

        
        pk_user = request.data['pk_user']
        fileProtocol = request.data['fileProtocol']
        public = request.FILES.get("public_key")
        private = request.FILES.get("private_key")
        password = request.data['password']

        
        firma = Firma.objects.filter(fk_user = pk_user, state = True).first()
        if  firma is None:
            return Response({'message':'Ocurrió una interrupcción en la busqueda de tu firma electronica, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        ruta_firma = firma.ruta_firma
        
        """
        archivo = open(firma.ruta_public_key, 'rb').read()
        cer_store_hash = SHA256.new(archivo)

        archivo = open(firma.ruta_private_key, 'rb').read()
        priv_store_hash = SHA256.new(archivo)

        """

        base         = Path(__file__).resolve().parent.parent.parent.parent.parent
        pathFile     = str(base) + str(fileProtocol)
        dir_protocol     = os.path.dirname(pathFile) +'/'+str(pk_user)+'/'

        
        os.system('rm '+dir_protocol+'*')
        fss         = FileSystemStorage(location = dir_protocol)
        certificado = fss.save(public.name, public)
        llave       = fss.save(private.name, private)


        in_certificado = dir_protocol + public.name + ''
        out_certificado = dir_protocol + 'public.pem'

        in_key = dir_protocol + private.name + ''
        out_key = dir_protocol + 'private.pem'

        try:
            os.system('openssl x509 -in '+ in_certificado +' -out '+out_certificado+'')
            f = open(out_certificado, "r")
            f.close()
        except:
            return Response({'message':'Ocurrió una interrupcción al cargar tu certificado, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            os.system('openssl pkcs8 -in '+in_key+' -out '+out_key+' -passin pass:'+password+'')
            f = open(out_key, "r")
            f.close()
        except:
            return Response({'message':'Contraseña de firma electrónica incorrecta'}, status = status.HTTP_400_BAD_REQUEST)




        
        f = open(out_key, 'r')
        keyPair = RSA.import_key(f.read())
        archivo = open(pathFile, 'rb').read()
        f.close()
        hash = SHA256.new(archivo)
        
        signer = PKCS115_SigScheme(keyPair)
        signature = signer.sign(hash)

        
        
        
        


        
        #f = open(out_certificado, 'r')
        
        f = open(ruta_firma+'public.pem', 'r')
        pubKey = RSA.import_key(f.read())
        f.close()

        
        archivo = open(pathFile, 'rb').read()
        hash2 = SHA256.new(archivo)

        verifier = PKCS115_SigScheme(pubKey)

        try:
            verifier.verify(hash2, signature)
            print('la firma es valida')
        except:
            print('la firma no es valida')
        
        

        

        


        """
        signature = base64.b64encode(signature)
        signature = signature.decode('utf-8')
        
        print( len(signature) ) 

        """

        
        
        """
        try:
            os.system('openssl x509 -in '+ in_certificado +' -out '+out_certificado+'')
            f = open(out_certificado, "r")
        except:
            return Response({'message':'Ocurrió una interrupcción al cargar tu certificado, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            os.system('openssl pkcs8 -in '+in_key+' -out '+out_key+' -passin pass:'+password+'')
            f = open(out_key, "r")
        except:
            return Response({'message':'Contraseña de firma electrónica incorrecta'}, status = status.HTTP_400_BAD_REQUEST)
        """

        """
        archivo = open(in_certificado, 'rb').read()
        cer_new_hash = SHA256.new(archivo)

        archivo = open(in_key, 'rb').read()
        priv_new_hash = SHA256.new(archivo)
        """
        

        

        
        #os.system(cadena)

        #in_key = base + key.name + ''
        #print(in_certificado)

        #f = open(in_certificado, "r")
        #print(f.read()) 

        #llave_publica = os.path.splitext(in_certificado)[0] +'.pem'
        #llave_publica = os.path.splitext(in_certificado)[0] +'.pem'
        #print(llave_publica)





        """
        fss         = FileSystemStorage(location = dir_protocol)
        certificado = fss.save(public.name, public)
        llave       = fss.save(private.name, private)
        """


        
        

         

        
        return Response({'message':'continua'}, status = status.HTTP_200_OK)
        

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


            
        
        