from rest_framework import routers
from main.views import ReportViewset

router = routers.DefaultRouter()
router.register(r'reports', ReportViewset, basename='report')
urlpatterns = router.urls