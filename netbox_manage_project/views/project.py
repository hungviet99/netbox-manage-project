from netbox.views import generic
from dcim.models import Device
from ipam.models import IPAddress
from virtualization.models import VirtualMachine
from .. import forms, models, tables


# Project view
class ProjectView(generic.ObjectView):
    queryset = models.Project.objects.all()

    def get_extra_context(self, request, instance):
        table = tables.UserTable(instance.user_project.all())
        table.configure(request)
        return {
            'user_tables': table,
        }


class ProjectListView(generic.ObjectListView):
    queryset = models.Project.objects.all()

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
    table = tables.ProjectTable


class ProjectEditView(generic.ObjectEditView):
    queryset = models.Project.objects.all()
    form = forms.ProjectForm


class ProjectDeleteView(generic.ObjectDeleteView):
    queryset = models.Project.objects.all()