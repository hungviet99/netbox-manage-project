from netbox.views import generic
from dcim.models import Device
from ipam.models import IPAddress
from virtualization.models import VirtualMachine
from .. import forms, models, tables
from django.db.models import Sum
# from django.contrib.contenttypes.models import ContentType
# from extras.models import CustomField
from tenancy.models import Contact
from tenancy.tables import ContactTable
from django.db.models import Count


# Project view
class ProjectView(generic.ObjectView):
    queryset = models.Project.objects.all()
    def get_extra_context(self, request, instance, **kwargs):
        contacts_list = instance.contact.all()
        table = ContactTable(Contact.objects.filter(
            pk__in=[contact.pk for contact in contacts_list]
            ).annotate(assignment_count=Count('assignments'))
        )
        table.configure(request)
        return {
            'table_user': table,
        }


class ProjectListView(generic.ObjectListView):
    queryset = models.Project.objects.all()
    
    def convert_mb_to_flexible_size(self, mb_value):
        if mb_value >= 1048576:
            # Convert from MB to TB
            tb_value = mb_value / 1024 / 1024
            return '{}TB'.format(int(tb_value))
        elif mb_value >= 1024:
            # Convert from MB to GB
            gb_value = mb_value / 1024
            return '{}GB'.format(int(gb_value))
        else:
            # No convert
            return '{}MB'.format(int(mb_value))

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for project in queryset:
            project.device_count = project.devices.all().count()
            project.ip_count = project.ipaddress.all().count()
            project.vm_count = project.virtualmachine.all().count()

            quota_templates = models.QuotaTemplate.objects.filter(id=project.quota_template_id).first()
            vms_list = project.virtualmachine.all()
            vms = VirtualMachine.objects.filter(
                    pk__in=[vm.pk for vm in vms_list]
                )
            result = vms.aggregate(total_ram=Sum('memory'), total_cpu=Sum('vcpus'))
            if result['total_cpu'] and result['total_ram']:
                total_cpu = result['total_cpu']
                total_ram = self.convert_mb_to_flexible_size(int(result['total_ram']))
            elif not result['total_cpu'] and not result['total_ram']:
                total_cpu = '0'
                total_ram = '0'
            elif result['total_cpu'] and not result['total_ram']:
                total_cpu = result['total_cpu']
                total_ram = '0'
            elif not result['total_cpu'] and result['total_ram']:
                total_cpu = '0'
                total_ram = self.convert_mb_to_flexible_size(int(result['total_ram']))
            ram_quota = self.convert_mb_to_flexible_size(int(quota_templates.ram_quota))
            project.ram_quota_used = "Assign {} of {}".format(
                str(total_ram),
                str(ram_quota)
            )
            project.cpu_quota_used = "Assign {} of {}".format(
                int(total_cpu),
                int(quota_templates.vcpus_quota)
            )

            project.disk_quota_used = "_"

            project.device_quota_used = "Assign {} of {}".format(
                int(project.device_count),
                int(quota_templates.device_quota)
            )
            project.vm_quota_used = "Assign {} of {}".format(
                int(project.vm_count),
                int(quota_templates.instances_quota)
            )
            project.ip_quota_used = "Assign {} of {}".format(
                int(project.ip_count),
                int(quota_templates.ipaddr_quota)
            )
            project.save()
        return queryset
    table = tables.ProjectTable


class ProjectEditView(generic.ObjectEditView):
    queryset = models.Project.objects.all()
    form = forms.ProjectForm


class ProjectDeleteView(generic.ObjectDeleteView):
    queryset = models.Project.objects.all()