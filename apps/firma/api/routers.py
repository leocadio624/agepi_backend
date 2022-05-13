from rest_framework.routers import DefaultRouter
from apps.firma.api.views.firma_views import (FirmaViewSet, FirmaPassViewSet, FirmaDownloadViewSet, verificaFirmaStartViewSet)

router = DefaultRouter()
router.register(r'firma', FirmaViewSet, basename = 'firma')
router.register(r'pass', FirmaPassViewSet, basename = 'pass')
router.register(r'descarga_firma', FirmaDownloadViewSet, basename = 'descarga_firma')
router.register(r'verificaFirmaStart', verificaFirmaStartViewSet, basename = 'verificaFirmaStart')
urlpatterns = router.urls
