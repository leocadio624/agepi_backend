from rest_framework.routers import DefaultRouter
from apps.team.api.views.team_views import TeamViewSet, teamListViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename = 'teams')
router.register(r'team_list', teamListViewSet, basename = 'team_list')
urlpatterns = router.urls
