from .models import Project, QuotaTemplate, ProjectStatusChoices
from extras.models import Tag
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from utilities.forms import ConfirmationForm, BootstrapMixin
from django import forms
from dcim.models import Device, DeviceRole, Platform, Rack, Region, Site, SiteGroup
from ipam.models import IPAddress
from tenancy.models import Contact
from virtualization.models import ClusterGroup, Cluster, VirtualMachine


class ProjectForm(NetBoxModelForm):
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    fieldsets = (
        (
            'General', 
            (
                'name', 
                'project_id', 
                'domain_name', 
                'status', 
                'quota_template'
            )
        ),
    )
    class Meta:
        model = Project
        fields = ('name', 'project_id', 'domain_name', 'status', 'quota_template', 'comments', 'tags')


class ProjectFilterForm(NetBoxModelFilterSetForm):
    model = Project
    name = forms.CharField(
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
    template_name = forms.CharField(
        label='Name',
    )
    instances_quota = forms.IntegerField(
        label='VM Quota',
        required=False,
    )

    vcpus_quota = forms.IntegerField(
        label='VCPUs Quota',
        required=False,
    )
    ram_quota = forms.IntegerField(
        label='RAM Quota (MB)',
        required=False,
    )
    ipaddr_quota = forms.IntegerField(
        label='IP Quota',
        required=False,
    )
    device_quota = forms.IntegerField(
        label='Device Quota',
        required=False,
    )
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    fieldsets = (
        (
            'General', 
            (
                'template_name', 
                'instances_quota', 
                'vcpus_quota', 
                'ram_quota', 
                'ipaddr_quota', 
                'device_quota'
            )
        ),
    )
    class Meta:
        model = QuotaTemplate
        fields = ('template_name', 'instances_quota', 'vcpus_quota', 'ram_quota', 'ipaddr_quota', 'device_quota', 'comments', 'tags')


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
    virtualmachine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        query_params={
            "vm_role": "True",
            'cluster_id': '$cluster'
        }
    )
    class Meta:
        fields = [
            'cluster', 'virtualmachine'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.fields['virtualmachine'].choices = []

class ProjectAddContactForm(BootstrapMixin, forms.Form):
    contact = DynamicModelMultipleChoiceField(
        queryset=Contact.objects.all(),
    )
    class Meta:
        fields = [
            'contact'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['contact'].choices = []

class DeletePJUserForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = []

    users = forms.ModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )