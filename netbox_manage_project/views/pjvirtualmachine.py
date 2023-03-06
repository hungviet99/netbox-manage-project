from netbox.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Project
from .. import forms, tables
from django.db import transaction
from virtualization.models import VirtualMachine
from virtualization.tables import VirtualMachineTable
from virtualization.filtersets import VirtualMachineFilterSet
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.views import ViewTab, register_model_view
from django.contrib import messages


@register_model_view(Project, 'instance')
class ProjectInstanceView(generic.ObjectChildrenView):
    queryset = Project.objects.all()
    child_model = VirtualMachine
    table = VirtualMachineTable
    filterset = VirtualMachineFilterSet
    template_name = 'project_views/instance.html'
    tab = ViewTab(
        label=_('VirtualMachine'),
        badge=lambda obj: obj.instance.count() if obj.instance else 0,
        weight=600
    )
     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        return VirtualMachine.objects.restrict(request.user, 'view').filter(
            custom_field_data__project='project_{}'.format(parent.pk)
        )



@register_model_view(Project, 'add_instance', path='instance/add')
class ProjectAddInstanceView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectAddInstanceForm
    template_name = 'project_views/project_add_instance.html'

    def get(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        project = get_object_or_404(queryset)
        form = self.form(initial=request.GET)

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': reverse('plugins:netbox_manage_project:project', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        project = get_object_or_404(queryset)
        form = self.form(request.POST)

        if form.is_valid():
            instance_pks = form.cleaned_data['instance']
            with transaction.atomic():
                # Assign the selected Instance to the Project
                for instance in VirtualMachine.objects.filter(pk__in=instance_pks):
                    custom_field_data = instance.custom_field_data
                    custom_field_data['project'] = 'project_{}'.format(pk)
                    instance.custom_field_data = custom_field_data
                    instance.save()
                # for pk in instance_pks:
                #     instance = VirtualMachine.objects.get(pk=pk)
                #     custom_field_data = instance.custom_field_data
                #     custom_field_data['project'] = 'project_{}'.format(pk)
                #     instance.custom_field_data = custom_field_data
                #     instance.save()
            messages.success(request, "Added {} instance to project {}".format(
                len(instance_pks), project
            ))
            return redirect(project.get_absolute_url())

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': project.get_absolute_url(),
        })

