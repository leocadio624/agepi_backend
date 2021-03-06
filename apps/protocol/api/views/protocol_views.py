from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.protocol.api.serializers.protocol_serializers import ProtocolSerializer, keyWordSerializer, WordListSerializer, SelectProtocoloSerializer, EvaluacionSerializer, PreguntaSerializer
from apps.protocol.api.serializers.catalogos_serializers import PeriodoListSerializer, InscripccionSerializer
from apps.team.api.serializers.team_serializers import TeamMemberSerializer
from apps.firma.api.serializers.firma_serializers import FirmaProtocoloSerializer
from apps.protocol.models import ProtocolState

from apps.team.models import TeamMembers
from apps.users.models import User

#Envio de correos
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




class ProtocolStartModuleViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodoListSerializer

    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def get_InscripcionQuery(self, pk = None):
        return InscripccionSerializer.Meta.model.objects.filter(state = True)
        
    #get
    def list(self, request):
        pk_user = request.GET["pk_user"]

        periodo_serializer = self.get_serializer(self.get_queryset(), many = True)
        inscripccion_serializer = InscripccionSerializer(self.get_InscripcionQuery(), many = True)

        team = TeamMembers.objects.filter(fk_user = pk_user, solicitudEquipo = 2, state = True).first()
        pk_team = team.fk_team.id if team else 0


        return Response({
            'periodos':periodo_serializer.data,
            'inscripcciones':inscripccion_serializer.data,
            'pk_team':pk_team
            }, status = status.HTTP_200_OK)


class ProtocolByTeamViewSet(viewsets.ModelViewSet):
    serializer_class = ProtocolSerializer

    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(fk_team = pk, state = True)


    #post
    def create(self, request):

        pk_team = request.data['pk_team']
        serializer = self.get_serializer(self.get_queryset(pk_team), many = True)
        
        return Response({
            'protocolo':serializer.data
            }, status = status.HTTP_200_OK)
        #return Response(serializer.data, status = status.HTTP_200_OK)

        

class ProtocolViewSet(viewsets.ModelViewSet):
    serializer_class = ProtocolSerializer

    """
    * Descripcion:  Envia correo electronico de que se ha creado un protocolo
    * Fecha de la creacion:     02/06/2022
    * Author:                   Eduardo B 
    """
    def enviarCorreo(self, fk_protocol):
        
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id = fk_protocol, state = True).first()
        titulo = protocolo.title
        numero = protocolo.number
        fk_team = protocolo.fk_team.id


        host = settings.EMAIL_HOST
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD


        
        
        

        miembros_equipo = TeamMemberSerializer.Meta.model.objects.filter(fk_team = fk_team, solicitudEquipo = 2, state= True)
        for i in miembros_equipo:

            receiver = i.fk_user.email
            receiver = 'leocadio624@gmail.com'

            
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = sender
            msg['Subject'] = 'Registro protocolo'
            

            
            email_body = 'Hola '+i.fk_user.name+' '+i.fk_user.last_name+' se ha registrado el protocolo con n??mero '+numero+' y de t??tulo '+titulo+''
            msg.attach(MIMEText(email_body, 'plain'))
            email_body_content = msg.as_string()

            server = smtplib.SMTP(host)
            server.starttls()

            server.login(sender, password)
            server.sendmail(sender, receiver, email_body_content)
            server.quit()
        



            



        



    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
    
    #get
    def list(self, request):
        protocol_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(protocol_serializer.data, status = status.HTTP_200_OK)

    #post
    def create(self, request):
                
        pk_user = request.data['pk_user']
        fk_periodo = request.data['fk_periodo']

        miembro_equipo = TeamMemberSerializer.Meta.model.objects.filter(fk_user = pk_user, solicitudEquipo = 2, state= True).first()

        if miembro_equipo is None:
            return Response({'message':'Para registrar un protocolo debes de estar relacionado en un equipo'}, status = status.HTTP_226_IM_USED)

        fk_team = str(miembro_equipo.fk_team.id)
        protocolo = self.get_serializer().Meta.model.objects.filter(fk_team=fk_team, state = True).first()
        
        if  protocolo:
            return Response({'message':'El equipo ya tiene un protocolo registrado'}, status = status.HTTP_226_IM_USED)
        
        directores = User.objects.filter(is_staff = True, rol_user = 2).values('id')
        miembro_equipo = TeamMemberSerializer.Meta.model.objects.filter(fk_team = fk_team, solicitudEquipo = 2, fk_user__in = directores,  state= True)

        if  len(miembro_equipo) == 0:
            return Response({'message':'Para registrar un protocolo tu equipo debe estar relacionado por al menos un profesor'}, status = status.HTTP_226_IM_USED)

        request.data['fk_team'] = fk_team

        serializer = self.serializer_class(data = request.data)
        nextProtocolo = len(self.get_queryset())

        keyWords = request.data['keyWords']
        keyWords = keyWords.split(',')

        #Se obtiene el anio del periodo de inscripccion
        periodo = PeriodoListSerializer.Meta.model.objects.filter(id = fk_periodo, state = True).first()
        nextProtocolo = 1 if nextProtocolo == 0 else nextProtocolo + 1
        nextProtocolo = "%03d" % (nextProtocolo,)

        nextProtocolo = 'A'+str(nextProtocolo) if request.data['fk_inscripccion'] == '1' else 'B'+str(nextProtocolo)
        nextProtocolo = str(periodo.anio)+'-'+nextProtocolo
        request.data['number'] = nextProtocolo
        
        if  serializer.is_valid():
            
            serializer.save()
            fk_Protocol = serializer.data['id']

            for word in keyWords:
                key_serializer = keyWordSerializer(data = {'word':word, 'fk_Protocol':fk_Protocol})
                if key_serializer.is_valid():
                    key_serializer.save()
            self.enviarCorreo(fk_Protocol)
            

            return Response({'message':'Protocolo registrado correctamente'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    
    #update
    def update(self, request, pk = None):
        if self.get_queryset(pk):
            protocol_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)

            if protocol_serializer.is_valid():
                protocol_serializer.save()

                fk_inscripccion = int( request.data['fk_inscripccion'] )
                if  fk_inscripccion == 2 or fk_inscripccion == 4:
                    self.resetProtocolo(pk)
                    

                palabras_clave = keyWordSerializer.Meta.model.objects.filter(fk_Protocol = pk, state = True).update(state = False)
                keyWords = request.data['keyWords']
                keyWords = keyWords.split(',')
                for word in keyWords:
                    key_serializer = keyWordSerializer(data = {'word':word, 'fk_Protocol':pk})
                    if key_serializer.is_valid():
                        key_serializer.save()

                return Response({'message':'Se ha actualizado el registro de protocolo'}, status = status.HTTP_200_OK)
            return Response({'message':'Ocurrio una interrupcci??n, intentelo m??s tarde'}, status = status.HTTP_400_BAD_REQUEST)

    def resetProtocolo(self, pk_protocol):

        estado = False
        FirmaProtocoloSerializer.Meta.model.objects.filter(fk_protocol = pk_protocol, state = True).update(state = estado)

        fk_protocol_state = ProtocolState.objects.filter(protocol_state = 2).first()
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id = pk_protocol, state = True).first()
        protocolo.fk_protocol_state = fk_protocol_state
        protocolo.save()

        select = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = pk_protocol, state = True).values('id')
        evaluaciones = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion__in = select, state = True)

        for i in evaluaciones:
            i.state = False
            i.save()

            PreguntaSerializer.Meta.model.objects.filter(fk_evaluacion = i.id, state = True).update(state = estado)
            
            

            

    def resetProtocolo2(self, pk_protocol):


        estado = True
        FirmaProtocoloSerializer.Meta.model.objects.filter(fk_protocol = pk_protocol, state = False).update(state = estado)
        
        fk_protocol_state = ProtocolState.objects.filter(protocol_state = 8).first()
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id = pk_protocol).first()
        
        protocolo.fk_protocol_state = fk_protocol_state
        protocolo.save()


        select = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = pk_protocol, state = True).values('id')
        evaluaciones = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion__in = select)

        for i in evaluaciones:
            i.state = True
            i.save()
            
            PreguntaSerializer.Meta.model.objects.filter(fk_evaluacion = i.id).update(state = estado)

            

    #delete
    def destroy(self, request, pk = None):
        protocol = self.get_queryset().filter(id = pk).first()
        if protocol:
            protocol.state = False
            protocol.save()
            return Response({'message':'Se ha eliminado el protocolo correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un protocolo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)



class keyWordViewSet(viewsets.ModelViewSet):
    serializer_class = keyWordSerializer
    
    
    def get_queryset(self, pk = None):
        
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:            
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()  


    def list(self, request):
        keyWord_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(keyWord_serializer.data, status = status.HTTP_200_OK)


    def create(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk = None):
        keyWord = self.get_queryset().filter(id = pk).first()

        if keyWord:
            keyWord.state = False
            keyWord.save()
            return Response(
                {
                'pk' : keyWord.id,
                'fk_protocol' : keyWord.fk_Protocol.id
                },
                status = status.HTTP_200_OK)
        return Response({'message':'No existe un protocolo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


class wordListViewSet(viewsets.ModelViewSet):
    serializer_class = keyWordSerializer

    def get_queryset(self, keyWord):
        return self.get_serializer().Meta.model.objects.filter(fk_Protocol = keyWord, state = True)

    def list(self, request):
        keyWord = request.GET["key"]
        keyWord_serializer = self.get_serializer(self.get_queryset(keyWord), many = True)
        return Response(keyWord_serializer.data, status = status.HTTP_200_OK)
        
        


    
  


