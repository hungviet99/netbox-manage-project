from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import F

from .. import models
from .serializers import ProjectSerializer, UserSerializer, QuotaTemplateSerializer
from django.db.models import Count, Subquery, OuterRef
from dcim.models import Device
from ipam.models import IPAddress
from virtualization.models import VirtualMachine

class ProjectViewSet(NetBoxModelViewSet):
    queryset = models.Project.objects.prefetch_related(
        'quota_template', 'tags'
    )
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for project in queryset:
            project.device_count = Device.objects.all().filter(
                custom_field_data__project='project_{}'.format(project.pk)
            ).count()
            project.ip_count = IPAddress.objects.all().filter(
                custom_field_data__project='project_{}'.format(project.pk)
            ).count()
            project.instance_count = VirtualMachine.objects.all().filter(
                custom_field_data__project='project_{}'.format(project.pk)
            ).count()
            project.save()
        return queryset
    serializer_class = ProjectSerializer


class QuotaTemplateViewSet(NetBoxModelViewSet):
    queryset = models.QuotaTemplate.objects.prefetch_related('tags')
    serializer_class = QuotaTemplateSerializer
    # filterset_class = filtersets.AccessListRuleFilterSet


class UserViewSet(NetBoxModelViewSet):
    queryset = models.User.objects.prefetch_related(
        'project', 'tags'
    )
    serializer_class = UserSerializer
    # filterset_class = filtersets.AccessListRuleFilterSet