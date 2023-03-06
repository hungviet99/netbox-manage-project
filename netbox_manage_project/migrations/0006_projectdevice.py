# Generated by Django 4.1.5 on 2023-03-05 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0167_module_status'),
        ('netbox_manage_project', '0005_project_devices'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDevice',
            fields=[
                ('device_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcim.device')),
                ('project', models.CharField(blank=True, default=None, max_length=20, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('dcim.device',),
        ),
    ]
