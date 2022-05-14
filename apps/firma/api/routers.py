from rest_framework.routers import DefaultRouter
from apps.firma.api.views.firma_views import (FirmaViewSet, FirmaPassViewSet, FirmaDownloadViewSet, verificaFirmaStartViewSet,
	 getIntegrantesProtocoloViewSet, verificaFirmaViewSet)

router = DefaultRouter()
router.register(r'firma', FirmaViewSet, basename = 'firma')
router.register(r'pass', FirmaPassViewSet, basename = 'pass')
router.register(r'descarga_firma', FirmaDownloadViewSet, basename = 'descarga_firma')
router.register(r'verificaFirmaStart', verificaFirmaStartViewSet, basename = 'verificaFirmaStart')
router.register(r'getIntegrantesProtocolo', getIntegrantesProtocoloViewSet, basename = 'getIntegrantesProtocolo')
router.register(r'verificaFirma', verificaFirmaViewSet, basename = 'verificaFirma')


urlpatterns = router.urls
