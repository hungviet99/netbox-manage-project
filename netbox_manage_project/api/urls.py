from netbox.api.routers import NetBoxRouter
from . import views
# from .serializers import ProjectSerializer, QuotaTemplateSerializer, UserSerializer

app_name = 'netbox_manage_project'

router = NetBoxRouter()
router.register('project', views.ProjectViewSet)
router.register('quotatemplate', views.QuotaTemplateViewSet)
router.register('user', views.UserViewSet)

# router.register_serializer('quotatemplate', QuotaTemplateSerializer)

urlpatterns = router.urls