from rest_framework.routers import DefaultRouter
from apps.protocol.api.views.protocol_views import ProtocolViewSet, keyWordViewSet, wordListViewSet, ProtocolStartModuleViewSet
from apps.protocol.api.views.catalogos_views import PeriodoViewSet, InscripccionViewSet

router = DefaultRouter()
router.register(r'protocolos', ProtocolViewSet, basename = 'protocolos')
router.register(r'palabras_clave', keyWordViewSet, basename = 'palabras_clave')
router.register(r'palabras_clave_list', wordListViewSet, basename = 'palabras_clave_list')
router.register(r'periodo', PeriodoViewSet, basename = 'periodo')
router.register(r'inscripccion', InscripccionViewSet, basename = 'inscripccion')
router.register(r'start_module', ProtocolStartModuleViewSet, basename = 'start_module')





urlpatterns = router.urls
