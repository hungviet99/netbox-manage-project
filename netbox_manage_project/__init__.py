from extras.plugins import PluginConfig


class NetBoxManageProjectConfig(PluginConfig):
    name = 'netbox_manage_project'
    verbose_name = 'NetBox Manage Project'
    description = 'Manage Create and Manage Project in Netbox'
    version = '1.1.1'
    base_url = 'netbox-project'
    min_version = '3.4.0'


config = NetBoxManageProjectConfig