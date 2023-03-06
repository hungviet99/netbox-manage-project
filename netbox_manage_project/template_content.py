from extras.plugins import PluginTemplateExtension
from .models import Project

class ProjectInfoExtension(PluginTemplateExtension):
    def left_page(self):
        object = self.context.get('object')
        project = Project.objects.filter(**{self.kind:object}).first()
        return self.render('netbox_manage_project/inc/project_info.html', extra_context={
            'project': project,
        })


class DeviceProjectInfo(ProjectInfoExtension):
    model = 'dcim.device'
    kind = 'devices'


class IPAddressProjectInfo(ProjectInfoExtension):
    model = 'ipam.IPAddress'
    kind = 'ipaddress'


class VirtualMachineProjectInfo(ProjectInfoExtension):
    model = 'virtualization.VirtualMachine'
    kind = 'instance'


template_extensions = (
    DeviceProjectInfo,
    IPAddressProjectInfo,
    VirtualMachineProjectInfo
)