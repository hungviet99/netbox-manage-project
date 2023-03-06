from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


class QuotaTemplate(NetBoxModel):
    template_name = models.CharField(
        max_length=100
    )
    instances_quota = models.PositiveIntegerField(
        blank=True
    )

    vcpus_quota = models.PositiveIntegerField(
        blank=True
    )

    ram_quota = models.PositiveIntegerField(
        blank=True
    )

    ipaddr_quota = models.PositiveIntegerField(
        blank=True
    )

    device_quota = models.PositiveIntegerField(
        blank=True
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('template_name',)

    def __str__(self):
        return str(f"{self.template_name}")

    def get_absolute_url(self):
        return reverse('plugins:netbox_manage_project:quotatemplate', args=[self.pk])
