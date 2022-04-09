from rest_framework.routers import DefaultRouter
from apps.protocol.api.views.protocol_views import ProtocolViewSet, keyWordViewSet, wordListViewSet

router = DefaultRouter()
router.register(r'protocolos', ProtocolViewSet, basename = 'protocolos')
router.register(r'palabras_clave', keyWordViewSet, basename = 'palabras_clave')
router.register(r'palabras_clave_list', wordListViewSet, basename = 'palabras_clave_list')


urlpatterns = router.urls
