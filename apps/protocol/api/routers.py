from rest_framework.routers import DefaultRouter
from apps.protocol.api.views.protocol_views import ProtocolViewSet, keyWordViewSet, wordListViewSet, ProtocolStartModuleViewSet, ProtocolByTeamViewSet
from apps.protocol.api.views.catalogos_views import PeriodoViewSet, InscripccionViewSet
from apps.protocol.api.views.firma_protocolos_views import (FirmaProtocolosViewSet, SolicitudesFirmaViewSet, existeFirmaViewSet, firmaDocumentoViewSet, 
		crearDocumentoFirmasViewSet, firmasQRViewSet)
from apps.protocol.api.views.line_protocol_views import (LineProtocolStartViewSet, getIntegrantesViewSet, getFirmasViewSet, verEvaluacionSinodalViewSet)
from apps.protocol.api.views.catt_protocolos_views import ( ProtocolCattStartViewSet, filtrarProtocolosViewSet, asignacionProtocoloViewSet, getFechaAsignacionViewSet, 
															getProfesoresSeleccionViewSet, getFechaEvaluacionViewSet, generarDictamenViewSet, verDictamenViewSet,
															asignacionAcademiasViewSet, selectProtocolViewSet, generarEvalucacionViewSet)
from apps.protocol.api.views.profesor_protocolos_views import protocolsProfesorInit



router = DefaultRouter()
router.register(r'protocolos', ProtocolViewSet, basename = 'protocolos')
router.register(r'protocolos', ProtocolViewSet, basename = 'protocolos')
router.register(r'palabras_clave', keyWordViewSet, basename = 'palabras_clave')
router.register(r'palabras_clave_list', wordListViewSet, basename = 'palabras_clave_list')
router.register(r'periodo', PeriodoViewSet, basename = 'periodo')
router.register(r'inscripccion', InscripccionViewSet, basename = 'inscripccion')
router.register(r'start_module', ProtocolStartModuleViewSet, basename = 'start_module')
router.register(r'team', ProtocolByTeamViewSet, basename = 'team')
router.register(r'solicta_firma', FirmaProtocolosViewSet, basename = 'solicta_firma')
router.register(r'solicitudes_firma', SolicitudesFirmaViewSet, basename = 'solicitudes_firma')
router.register(r'existeFirma', existeFirmaViewSet, basename = 'existeFirma')
router.register(r'firmaDocumento', firmaDocumentoViewSet, basename = 'firmaDocumento')
router.register(r'crearDocumentoFirmas', crearDocumentoFirmasViewSet, basename = 'crearDocumentoFirmas')
router.register(r'firmasQR', firmasQRViewSet, basename = 'firmasQR')
router.register(r'LineProtocolStart', LineProtocolStartViewSet, basename = 'LineProtocolStart')
router.register(r'getIntegrantes', getIntegrantesViewSet, basename = 'getIntegrantes')
router.register(r'getFirmas', getFirmasViewSet, basename = 'getFirmas')
router.register(r'verEvaluacionSinodal', verEvaluacionSinodalViewSet, basename = 'verEvaluacionSinodal')
router.register(r'ProtocolCattStart', ProtocolCattStartViewSet, basename = 'ProtocolCattStart')
router.register(r'filtrarProtocolos', filtrarProtocolosViewSet, basename = 'filtrarProtocolos')
router.register(r'asignacionProtocolo', asignacionProtocoloViewSet, basename = 'asignacionProtocolo')
router.register(r'getFechaAsignacion', getFechaAsignacionViewSet, basename = 'getFechaAsignacion')
router.register(r'getProfesoresSeleccion', getProfesoresSeleccionViewSet, basename = 'getProfesoresSeleccion')
router.register(r'getFechaEvaluacion', getFechaEvaluacionViewSet, basename = 'getFechaEvaluacion')

router.register(r'generarDictamen', generarDictamenViewSet, basename = 'generarDictamen')
router.register(r'verDictamen', verDictamenViewSet, basename = 'verDictamen')



router.register(r'asignacionAcademias', asignacionAcademiasViewSet, basename = 'asignacionAcademias')
router.register(r'protocolsProfesorInit', protocolsProfesorInit, basename = 'protocolsProfesorInit')
router.register(r'selectProtocol', selectProtocolViewSet, basename = 'selectProtocol')
router.register(r'generarEvalucacion', generarEvalucacionViewSet, basename = 'generarEvalucacion')

urlpatterns = router.urls
#'/protocolos/start_module/'


