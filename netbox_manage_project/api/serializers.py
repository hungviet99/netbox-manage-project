from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Project, QuotaTemplate, User


class NestedProjectSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_manage_project-api:project-detail'
    )
    device_count = serializers.IntegerField(read_only=True)
    ip_count = serializers.IntegerField(read_only=True)
    instance_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'url', 'display', 'name', 'device_count', 'ip_count', 'instance_count')


class NestedQuotaTemplateSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_manage_project-api:quotatemplate-detail'
    )

    class Meta:
        model = QuotaTemplate
        fields = ('id', 'url', 'display', 'template_name')

class NestedUserSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_manage_project-api:user-detail'
    )

    class Meta:
        model = User
        fields = ('id', 'url', 'display', 'user_name')

class ProjectSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_manage_project-api:project-detail'
    )
    quota_template = NestedQuotaTemplateSerializer()
    device_count = serializers.IntegerField(read_only=True)
    ip_count = serializers.IntegerField(read_only=True)
    instance_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Project
        fields = (
            'id', 'url', 'display', 'name', 'project_id', 'status', 'quota_template',
            'domain_name', 'description', 'device_count', 'ip_count', 'instance_count',
            'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )

class UserSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_manage_project-api:user-detail'
    )
    project = NestedProjectSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'url', 'display', 'user_name', 'project', 'phone', 'mail', 'address',
            'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )

class QuotaTemplateSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_manage_project-api:quotatemplate-detail'
    )

    class Meta:
        model = QuotaTemplate
        lookup_field = 'template_name'
        fields = (
            'id', 'url', 'display', 'template_name', 'instances_quota', 
            'vcpus_quota', 'ram_quota', 'ipaddr_quota', 'device_quota', 
            'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )