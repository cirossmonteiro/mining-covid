from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from main.views import ReportViewset, FileViewset

router = routers.DefaultRouter()
router.register(r'reports', ReportViewset, basename='report')
# router.register(r'files', FileViewset, basename='file')
urlpatterns = router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)