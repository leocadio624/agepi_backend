from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.notification.api.serializers.notificacion_serializers import NotificacionTeamSerializer, SolicitudFirmaSerializer

from apps.protocol.api.serializers.protocol_serializers import ProtocolSerializer
from apps.protocol.models import ProtocolState
from apps.team.models import TeamMembers


from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.http import HttpResponse
from wsgiref.util import FileWrapper

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

    """
    * Descripcion: Descarga archivo en modulo
    * solicitudes firma
    * Fecha de la creacion:     06/05/2022
    * Author:                   Eduardo B 
    """
    def create(self, request):

        pk_protocol = request.data['pk_protocol']
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id = pk_protocol).first()


        if  protocolo:

            path = protocolo.fileProtocol
            base = Path(__file__).resolve().parent.parent.parent
            pathFile  = str(base) + path

            print(pathFile)
            
            """
            document = open(path, 'rb')
            print(document)
            response = HttpResponse(FileWrapper(document), content_type='application/msword')
            response['Content-Disposition'] = 'attachment'
            return response
            """


        else:
            print('no existe el protocolo')

        return Response({'message':'mensaje generico'}, status = status.HTTP_200_OK)


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


            
        
        