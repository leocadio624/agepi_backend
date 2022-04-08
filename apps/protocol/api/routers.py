from rest_framework.routers import DefaultRouter
from apps.protocol.api.views.protocol_views import ProtocolViewSet, keyWordViewSet

router = DefaultRouter()
router.register(r'protocolos', ProtocolViewSet, basename = 'protocolos')
router.register(r'palabras_clave', keyWordViewSet, basename = 'palabras_clave')


urlpatterns = router.urls
