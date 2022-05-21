from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.protocol.api.serializers.protocol_serializers import ProtocolSerializer, AsignacionProtocoloSerializer
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


