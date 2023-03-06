from .models import Project, QuotaTemplate, User, ProjectStatusChoices
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms import ConfirmationForm, BootstrapMixin
from django import forms
from dcim.models import Device, DeviceRole, Platform, Rack, Region, Site, SiteGroup
from ipam.models import IPAddress
from virtualization.models import ClusterGroup, Cluster, VirtualMachine


class ProjectForm(NetBoxModelForm):
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    class Meta:
        model = Project
        fields = ('name', 'project_id', 'domain_name', 'status', 'quota_template', 'comments', 'tags')


class ProjectFilterForm(NetBoxModelFilterSetForm):
    model = Project
    name = forms.CharField(
        required=False,
    )
    project_id = forms.CharField(
        required=False,
    )
    status = forms.MultipleChoiceField(
        choices=ProjectStatusChoices,
        required=False,
    )
    quota_template = DynamicModelChoiceField(
        queryset=QuotaTemplate.objects.all(),
        required=False,
    )

class QuotaTemplateForm(NetBoxModelForm):
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    class Meta:
        model = QuotaTemplate
        fields = ('template_name', 'instances_quota', 'vcpus_quota', 'ram_quota', 'ipaddr_quota', 'device_quota', 'comments', 'tags')

class UserForm(NetBoxModelForm):
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    class Meta:
        model = User
        fields = ('user_name', 'project', 'phone', 'mail', 'address', 'comments', 'tags')

class UserFilterForm(NetBoxModelFilterSetForm):
    model = User

    project = DynamicModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
    )
    user_name = forms.CharField(
        required=False,
    )

###### Project Device ######

### Device ADD
class ProjectAddDevicesForm(BootstrapMixin, forms.Form):
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        null_option='None'
    )
    site_group = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        null_option='None'
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region',
            'group_id': '$site_group',
        }
    )
    rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site'
        }
    )
    devices = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        query_params={
            'site_id': '$site',
            'rack_id': '$rack',
        }
    )

    class Meta:
        fields = [
            'region', 'site', 'rack', 'devices',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['devices'].choices = []

### Device Remove

class ProjectRemoveDevicesForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Device.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


###### Project IPAddress ######

### Device ADD
class ProjectAddIPAddressForm(BootstrapMixin, forms.Form):
    ipaddress = DynamicModelMultipleChoiceField(
        queryset=IPAddress.objects.all(),
    )
    class Meta:
        fields = [
            'ipaddress'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['ipaddress'].choices = []



###### Project Instance ######

### Instance ADD
class ProjectAddInstanceForm(BootstrapMixin, forms.Form):
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all()
    )
    instance = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        query_params={
            "vm_role": "True",
            'cluster_id': '$cluster'
        }
    )
    class Meta:
        fields = [
            'cluster', 'instance'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['instance'].choices = []