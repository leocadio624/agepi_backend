import os
from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from apps.firma.models import Firma
from apps.comunidad.models import Alumno, Profesor

from apps.firma.api.serializers.firma_serializers import FirmaSerializer
from django.utils import timezone
from datetime import date


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

        ruta            = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/'
        path_public     = ruta = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/' + public
        path_private    = ruta = str(settings.BASE_DIR) + '/firmas/' + str(fk_user)+ '/' + private


        cadena = 'openssl req -x509 -inform der -sha1 -days '+delta+' -newkey rsa:2048 -passout pass:'+password+''
        cadena += ' -subj "/C=MX/ST=CIUDAD DE MEXICO/L=GAM/O=AGEPI/OU=IT Department AGEPI/CN=AUTORIDAD NO CERTIFICADORA"'
        cadena += ' -inform der -keyout '+path_private+' -out '+path_public+''
        os.system(cadena)

    
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
                                            'vigencia_firma'    :date2})
        if  serializer.is_valid():
            #print( serializer.is_valid() )
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

        

