from django.db import models
from django.urls import reverse
from dcim.models import Device
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
# from netbox_manage_project.models.quotatemplate import QuotaTemplate
from .quotatemplate import QuotaTemplate

class ProjectStatusChoices(ChoiceSet):

    CHOICES = [
        ('active', 'Active', 'blue'),
        ('disable', 'Disable', 'red'),
    ]


class Project(NetBoxModel):
    name = models.CharField(
        max_length=100
    )

    project_id = models.CharField(
        max_length=100,
        blank=True
    )

    domain_name = models.CharField(
        max_length=50,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=ProjectStatusChoices
    )

    quota_template = models.ForeignKey(
        to='netbox_manage_project.QuotaTemplate',
        on_delete=models.SET_NULL,
        related_name='project_quota',
        null=True
    )
    devices = models.ForeignKey(
        to='dcim.Device', 
        on_delete=models.CASCADE, 
        related_name='assigned_device',
        blank=True,
        null=True,
        default=None
    )
    ipaddress = models.ForeignKey(
        to='ipam.IPAddress', 
        on_delete=models.CASCADE, 
        related_name='assigned_ipaddress',
        blank=True,
        null=True,
        default=None
    )
    instance = models.ForeignKey(
        to='virtualization.VirtualMachine', 
        on_delete=models.CASCADE, 
        related_name='assigned_instance',
        blank=True,
        null=True,
        default=None
    )
    description = models.CharField(
        max_length=500,
        blank=True
    )
    device_count = models.IntegerField(null=True, blank=True, default=None)
    ip_count = models.IntegerField(null=True, blank=True, default=None)
    instance_count = models.IntegerField(null=True, blank=True, default=None)
    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(f"{self.name}")
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_manage_project:project', args=[self.pk])

    def get_status_color(self):
        return ProjectStatusChoices.colors.get(self.status)