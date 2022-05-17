from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.notification.api.serializers.notificacion_serializers import NotificacionTeamSerializer, SolicitudFirmaSerializer
from apps.firma.api.serializers.firma_serializers import FirmaProtocoloSerializer, FirmaPDFSerializer, FirmaQrSerializer

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
import base64

#generar pdf de firmas
import pdfkit
import qrcode
from PyPDF2 import PdfFileMerger

#UTC
import pytz
import datetime
#from datetime import datetime
from django.utils import timezone




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

    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%Y-%m-%d %H:%M:%S')


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

    def convertUTC(self, date):
        fmt = '%d/%m/%Y %H:%M'
        utc = date.replace(tzinfo=pytz.UTC)
        localtz = utc.astimezone(timezone.get_current_timezone())
        return localtz.strftime('%Y-%m-%d %H:%M:%S')


    def actualizaEstadoProtocolo(self, fk_protocol):

        #firmado parcialmente
        estado_protocolo = 3
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id = fk_protocol, state = True).first()
        fk_team = protocolo.fk_team.id

        integrantes = TeamMemberSerializer.Meta.model.objects.filter(fk_team = fk_team, solicitudEquipo = 2, state = True)
        numIntegrantes = len(integrantes)


        firmas_protocolo = FirmaProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True)
        numFirmas = len(firmas_protocolo)

        #firmado por todos los integrantes
        if numIntegrantes == numFirmas : estado_protocolo = 4

        fk_protocol_state = ProtocolState.objects.filter(protocol_state = estado_protocolo).first()
        protocolo.fk_protocol_state = fk_protocol_state
        protocolo.save()



    def vigenciaFirma(self, start_date, vigencia):

        start_date = self.convertUTC(start_date)
        time_created = start_date.split(' ')
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

        vigencia_str = vigencia.strftime('%Y-%m-%d') +' '+time_created[1]
        end_date = datetime.datetime.strptime(vigencia_str, "%Y-%m-%d %H:%M:%S")        
        now = datetime.datetime.now()
        #now = datetime.datetime.strptime('2023-05-08 16:08:09', "%Y-%m-%d %H:%M:%S")

        if start_date < now < end_date:
            return True
        else:
            return False



    def create(self, request):
        
        pk_user         = request.data['pk_user']
        pk_protocol     = request.data['pk_protocol']
        fileProtocol    = request.data['fileProtocol']
        private         = request.FILES.get("private_key")
        password        = request.data['password']

        firma = Firma.objects.filter(fk_user = pk_user, state = True).first()

        if  firma is None:
            return Response({'message':'Ocurrió una interrupcción en la comprobación de tu firma electronica, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)
        
        if  self.vigenciaFirma(firma.created_date, firma.vigencia_firma) == False:
            return Response({'message':'La vigencia de tu firma electrónica ha vencido'}, status = status.HTTP_400_BAD_REQUEST)


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
                self.actualizaEstadoProtocolo(pk_protocol)
                return Response({'message':'Se ha firmado el protocolo correctamente'}, status = status.HTTP_200_OK)
            return Response({'message':'Ocurrio una interrupcción, favor de intentarlo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)    

        except Exception as e:
            print(str(e))
            return Response({'message':'La clave privada proporcionada no te pertenece'}, status = status.HTTP_400_BAD_REQUEST)

                
        """
        """
            

class crearDocumentoFirmasViewSet(viewsets.ModelViewSet):
    serializer_class = FirmaPDFSerializer
    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(fk_protocol = pk, state = True)


    def get_image_file_as_base64_data(self, ruta):
        with open(ruta, 'rb') as image_file:
            salida = base64.b64encode(image_file.read())
            salida = salida.decode('UTF-8')
            return salida
    """
    pk = pk_protocol.encode('UTF-8')
    pk = base64.b64decode(pk)
    pk = pk.decode('UTF-8')
    MTY=
    """
    def create(self, request):

        
        fileProtocol    = request.data['fileProtocol']
        pk_protocol     = request.data['pk_protocol']
        serializer = self.get_serializer(self.get_queryset(pk_protocol), many = True)

        argument_url = bytes(str(pk_protocol), 'utf-8')
        argument_url = base64.b64encode(argument_url)
        argument_url = argument_url.decode('UTF-8')

        

        base            = Path(__file__).resolve().parent.parent.parent.parent.parent
        pathFile        = str(base) + str(fileProtocol)
        pathQr              = os.path.dirname(os.path.realpath(pathFile)) + '/qrcode.png'


        input_data = 'http://localhost:3000/validar_firmas_priv_qr/'+argument_url
        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=0)

        qr.add_data(input_data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(pathQr)


        dir_pdf         = os.path.dirname(os.path.realpath(pathFile)) + '/firmas.pdf'
        salida_pdf         = os.path.dirname(os.path.realpath(pathFile)) + '/salida.pdf'
        index           = os.path.dirname(os.path.realpath(pathFile)) + '/index.html'
        
        aviso_priv = str(base) + '/aviso_priv.png'
        data_aviso = self.get_image_file_as_base64_data(aviso_priv)
        data_qr    = self.get_image_file_as_base64_data(pathQr)
        
        
        htmlstr = '<!doctype html>'
        htmlstr +='<html lang="en">'
        htmlstr +='<head>'
        htmlstr +='<meta charset="utf-8">'
        htmlstr +='<meta name="viewport" content="width=device-width, initial-scale=1">'
        htmlstr +='<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">'
        htmlstr +='</head>'
        htmlstr +='<body>'

        htmlstr +='<div style = "margin:30px;" >'
        for i in serializer.data:

            
            htmlstr +='<div style = "font-size:11px; margin-top:20px;">'+i['name']+'</div>'
            htmlstr +='<div style = "font-size:11px;" >'+i['last_name']+'</div>'
            htmlstr +='<div style = "font-size:11px;" >tel. '+i['phone']+'</div>'
            htmlstr +='<div style = "font-size:11px;" >'+i['email']+'</td>'
            htmlstr +='<div style = "font-size:11px;" >Boleta '+i['boleta']+'</td>'
            

            htmlstr +='<div style = "font-size:11px; width:40%; font-style:italic; text-justify; text-justify:inter-word;">'+i['summary']+'</div>'
            htmlstr +='<div style = "font-size:10px; margin-top:5px;"><strong>Sello digital</strong></div>'
            htmlstr +='<div class = "text-justify" style = "font-size:10px; word-wrap:break-word;">'+i['firma']+'</div>'

            htmlstr +='</div>'

        htmlstr +='<div class = "row" style = "margin-top:20px;">'
        htmlstr +=  '<div class = "col-6 d-flex justify-content-start">'
        htmlstr +=      '<img height = "100" width = "100" src="data:image/png;base64,'+data_qr+'" alt = "Aviso de privacidad" >'
        htmlstr +=  '</div>'

        htmlstr +=  '<div class = "col-6 d-flex justify-content-end">'
        htmlstr +=      '<img height = "85" width = "400" src="data:image/png;base64,'+data_aviso+'" alt = "Aviso de privacidad" >'
        htmlstr +=  '</div>'


        htmlstr +='</div>'
        htmlstr +='<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>'
        htmlstr +='</body'
        htmlstr +='</html>'
        pdfkit.from_string(htmlstr, dir_pdf)

        
        pdfs = []

        pdfs.append(pathFile)
        pdfs.append(dir_pdf)

        fusionador = PdfFileMerger()

        for pdf in pdfs:
            fusionador.append(open(pdf, 'rb'))

        with open(salida_pdf, 'wb') as salida:
            fusionador.write(salida)


        document = open(salida_pdf, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment'
        return response
        

class firmasQRViewSet(viewsets.ModelViewSet):
    serializer_class = FirmaQrSerializer
    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(fk_protocol = pk, state = True)


    def create(self, request):

        pk_protocol = request.data['pk_protocol']
        pk = pk_protocol.encode('UTF-8')
        pk = base64.b64decode(pk)
        pk = pk.decode('UTF-8')

        
        base         = Path(__file__).resolve().parent.parent.parent.parent.parent
        protocolo    = ProtocolSerializer(ProtocolSerializer.Meta.model.objects.filter(id = pk, state = True).first(), many = False)
        fileProtocol = protocolo.data['fileProtocol']

        pathFile    = str(base) + str(fileProtocol)
        archivo     = open(pathFile, 'rb').read()
        hash        = SHA256.new(archivo)



        serializer = self.get_serializer(self.get_queryset(pk), many = True)
        for i in serializer.data:

            signature = i['firma']
            signature = signature.encode('UTF-8')
            signature = base64.b64decode(signature)            


            ruta_firma = i['ruta_firma'] + 'public.pem'
            f = open(ruta_firma, 'r')
            pubKey = RSA.import_key(f.read())
            f.close()
            verifier = PKCS115_SigScheme(pubKey)

            try:
                verifier.verify(hash, signature)
                i['is_valid'] = 1

            except:
                i['is_valid'] = 0

        return Response(serializer.data, status = status.HTTP_200_OK)




        
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
            protocolo.save()
            

            
            for i in integrantes:
                notificacion_serilizer   = NotificacionTeamSerializer(data = {'fk_userOrigen':fk_userOrigen, 'fk_userDestino':i.id, 'fk_tipoNotificacion':4})
                if  notificacion_serilizer.is_valid():
                    notificacion_serilizer.save()
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


            
        
        