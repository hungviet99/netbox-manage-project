import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn, columns
from .models import Project, QuotaTemplate, User

__all__ = (
    'ProjectTable',
    'QuotaTemplateTable',
    'UserTable',
)

class ProjectTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )
    project_id = tables.Column(
    )
    domain_name = tables.Column(
    )
    status = ChoiceFieldColumn()

    quota_template = tables.Column(
        linkify=True,
    )

    device_count = tables.Column(
    )

    ip_count = tables.Column(
    )

    instance_count = tables.Column(
    )

    description = tables.Column()

    comments = columns.MarkdownColumn()
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        model = Project
        fields = ("pk", 
                  "id", 
                  "name", 
                  "project_id", 
                  "domain_name", 
                  "status", 
                  "quota_template", 
                  "device_count",
                  "ip_count",
                  "instance_count",
                  "description", 
                  "comments",
                  "tags", 
                  "created", 
                  "last_updated", 
                  "actions"
                )
        default_columns = ("name", 
                           "project_id", 
                           "domain_name", 
                           "status", 
                           "quota_template", 
                           "device_count",
                           "ip_count",
                           "instance_count",
                        )

class QuotaTemplateTable(NetBoxTable):
    template_name = tables.Column(
        linkify=True,
    )

    instances_quota = tables.Column()

    vcpus_quota = tables.Column()

    ram_quota = tables.Column()

    ipaddr_quota = tables.Column()

    device_quota = tables.Column()

    comments = columns.MarkdownColumn()
    tags = columns.TagColumn()
    class Meta(NetBoxTable.Meta):
        model = QuotaTemplate
        fields = (
            'id',
            'template_name',
            'instances_quota',
            'vcpus_quota',
            'ram_quota',
            'ipaddr_quota',
            'device_quota',
            'comments',
            'tags',
            'created',
            'last_updated',
            'actions',
        )
        default_columns = (
            'template_name',
            'instances_quota',
            'vcpus_quota',
            'ram_quota',
            'ipaddr_quota',
            'device_quota',
        )

class UserTable(NetBoxTable):
    user_name = tables.Column(
        linkify=True,
    )
    project = tables.Column(
        linkify=True,
    )

    phone = tables.Column()

    mail = tables.Column()

    address = tables.Column()

    comments = columns.MarkdownColumn()
    tags = columns.TagColumn()
    class Meta(NetBoxTable.Meta):
        model = User
        fields = (
            'id',
            'user_name',
            'project',
            'phone',
            'mail',
            'address',
            'comments',
            'tags',
            'created',
            'last_updated',
            'actions',
        )
        default_columns = (
            'user_name',
            'project',
            'phone',
            'mail',
            'address',
        )