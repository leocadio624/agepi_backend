import pytz
from django.utils import timezone

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.protocol.api.serializers.protocol_serializers import (ProtocolSerializer, AsignacionProtocoloSerializer,
                                                                SelectProtocoloSerializer, SelectProtocoloLineSerializer, EvaluacionSerializer, PreguntaSerializer)
from apps.protocol.api.serializers.catalogos_serializers import PeriodoListSerializer, ProtocolStateSerializer, AcademiaSerializer



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
    serializer_class = SelectProtocoloLineSerializer

    def get_queryset(self, pk = None):
        return self.serializer_class().Meta.model.objects.filter(fk_protocol = pk, state = True).order_by('created_date')

    def create(self, request):
        fk_protocol = request.data['fk_protocol']
        serializador = self.serializer_class(self.get_queryset(fk_protocol), many = True)

        last = len(serializador.data) - 1
        fecha_evaluacion = serializador.data[last]['fecha_evaluacion']
        
        return Response({'fecha_evaluacion':fecha_evaluacion},status = status.HTTP_200_OK)


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
                
            return Response({'message':'Se ha seleccionado el protocolo correctamente'},status = status.HTTP_200_OK)
        return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)



"""
* Descripcion: Genera evaluacion por parte de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class generarEvalucacionViewSet(viewsets.ModelViewSet):
    #serializer_class = SelectProtocoloSerializer

    def create(self, request):

        fk_user     = request.data['fk_user']
        fk_protocol = request.data['fk_protocol']
        fk_protocol_state = 0
        preguntas   = request.data['preguntas']
        summary     = request.data['summary'] 
        primera_evaluacion = [1,3]
        version = 0
        
        
        protocol = ProtocolSerializer.Meta.model.objects.filter(id = fk_protocol, state = True).first()
        if protocol is None:   
            return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        fk_protocol_state = protocol.fk_protocol_state.id
        if protocol.fk_inscripccion.id in primera_evaluacion:
            version = 1
        else:
            version = 2
    
        dictamen = True
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

                if  estado == False:
                    dictamen = False

                pregunta_serializer = PreguntaSerializer(data = {'fk_evaluacion':fk_evaluacion, 'numPregunta':numPregunta, 'estado':estado, 'observacion':observacion})
                if  pregunta_serializer.is_valid():
                    pregunta_serializer.save()

            #actualiza dictamen
            evaluacion = EvaluacionSerializer.Meta.model.objects.filter(id = fk_evaluacion).first()
            evaluacion.dictamen = dictamen
            evaluacion.save()

            #actualiza estado de protocolos que ya estan seleccionados '6'
            if  fk_protocol_state == 6:
                selecciones = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True).values('id')
                evaluaciones = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion__in = selecciones, state = True)

                if  len(evaluaciones) == 3:
                    fk_protocol_state = ProtocolStateSerializer.Meta.model.objects.filter(protocol_state = 7).first()
                    protocolo = ProtocolSerializer.Meta.model.objects.filter(id  = fk_protocol, state = True).first()
                    protocolo.fk_protocol_state = fk_protocol_state
                    protocolo.save()

            return Response({'message':'Se ha generado la evaluación correctamente'},status = status.HTTP_200_OK)            
        return Response({'message':'Ocurrió una interrupcción, intentelo mas tarde'}, status = status.HTTP_400_BAD_REQUEST)

        
"""
* Descripcion: Genera tabla con evaluacion de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
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
* Descripcion: Genera tabla con evaluacion de sinodal
* Fecha de la creacion:     24/05/2022
* Author:                   Eduardo Bernal Leocadio
"""
class generarDictamenViewSet(viewsets.ModelViewSet):

    def create(self, request):
        
        """
        fk_protocol = request.data['fk_protocol']

        select = SelectProtocoloSerializer.Meta.model.objects.filter(fk_protocol = fk_protocol, state = True).values('id')
        evaluaciones = EvaluacionSerializer.Meta.model.objects.filter(fk_seleccion__in = select, state = True)

        dictamen = True
        for i in evaluaciones:
            if i.dictamen == False : dictamen = False

        fk_protocol_state = ProtocolStateSerializer.Meta.model.objects.filter(protocol_state = 7).first()
        protocolo = ProtocolSerializer.Meta.model.objects.filter(id  = fk_protocol, state = True).first()
        protocolo.dictamen = dictamen
        protocolo.fk_protocol_state = fk_protocol_state
        protocolo.save()

        
        """
        
        return Response({'message':'generarDictamenViewSet'},status = status.HTTP_200_OK)        


