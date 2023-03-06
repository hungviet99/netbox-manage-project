from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from .project import Project

class User(NetBoxModel):
    user_name = models.CharField(
        max_length=100
    )

    project = models.ForeignKey(
        to='netbox_manage_project.Project',
        on_delete=models.PROTECT,
        related_name='user_project'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    mail = models.CharField(
        max_length=50,
        blank=True
    )

    address = models.CharField(
        max_length=200,
        blank=True
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('user_name',)

    def __str__(self):
        return str(f"{self.user_name}")
        
    def get_absolute_url(self):
        return reverse('plugins:netbox_manage_project:user', args=[self.pk])