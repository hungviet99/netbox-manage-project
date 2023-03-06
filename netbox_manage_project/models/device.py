from django.db import models
from dcim.models import Device

class ProjectDevice(Device):
    project = models.CharField(max_length=20, blank=True, default=None, null=True)
