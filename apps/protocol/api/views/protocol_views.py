from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.base.api import GeneralListApiView
from apps.users.authentication_mixins import Authentication
from apps.protocol.api.serializers.protocol_serializers import ProtocolSerializer, keyWordSerializer

#class ProtocolViewSet(Authentication, viewsets.ModelViewSet):
class ProtocolViewSet(viewsets.ModelViewSet):
    serializer_class = ProtocolSerializer
    #serializer_class_ = keyWordSerializer
    
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
        
        
        serializer = self.serializer_class(data = request.data)
        nextProtocolo = len(self.get_queryset())


        keyWords = request.data['keyWords']
        keyWords = keyWords.split(',')

        if nextProtocolo == 0:  
            nextProtocolo = 1
        else:
            nextProtocolo = nextProtocolo + 1
        
        nextProtocolo = "%02d" % (nextProtocolo,)
        request.data['number'] = nextProtocolo


        if serializer.is_valid():

            serializer.save()
            fk_Protocol = serializer.data['id']

            for word in keyWords:
                key_serializer = keyWordSerializer(data = {'word':word, 'fk_Protocol':fk_Protocol})
                if key_serializer.is_valid():
                    key_serializer.save()
            
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        

    
    #update
    def update(self, request, pk = None):
        if self.get_queryset(pk):
            protocol_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if protocol_serializer.is_valid():
                protocol_serializer.save()
                return Response(protocol_serializer.data, status = status.HTTP_200_OK)
            return Response(protocol_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
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
        """
        print(serializer.is_valid())
        """
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        #return Response({'message':'respuesta generica'}, status = status.HTTP_200_OK)


""" 
class ProtocolListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProtocolSerializer
    queryset = ProtocolSerializer.Meta.model.objects.filter(state = True)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Protocolo creado'}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProtocolSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()

    def patch(self, request, pk = None):
        if self.get_queryset(pk):
            protocol_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(protocol_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe un producto con estos datos'}, status = status.HTTP_200_OK)
    
    def put(self, request, pk = None):
        if self.get_queryset(pk):
            protocol_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if protocol_serializer.is_valid():
                protocol_serializer.save()
                return Response(protocol_serializer.data, status = status.HTTP_200_OK)
            return Response(protocol_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk = None):
        protocol = self.get_queryset().filter(id = pk).first()
        if protocol:
            protocol.state = False
            protocol.save()
            return Response({'message':'Se ha eliminado el protocolo correctamente'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe un protocolo con estos datos'}, status = status.HTTP_400_BAD_REQUEST)
"""

    
  


