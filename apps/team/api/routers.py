from rest_framework.routers import DefaultRouter
from apps.team.api.views.team_views import TeamViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename = 'teams')
urlpatterns = router.urls
