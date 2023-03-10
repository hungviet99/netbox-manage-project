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


@register_model_view(Project, 'virtualmachine')
class ProjectInstanceView(generic.ObjectChildrenView):
    queryset = Project.objects.all()
    child_model = VirtualMachine
    table = VirtualMachineTable
    filterset = VirtualMachineFilterSet
    template_name = 'project_views/virtualmachine.html'
    tab = ViewTab(
        label=_('VirtualMachine'),
        badge=lambda obj: obj.virtualmachine.count() if obj.virtualmachine else 0,
        weight=600
    )
     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        vms_list = parent.virtualmachine.all()
        return VirtualMachine.objects.restrict(request.user, 'view').filter(
            pk__in=[vm.pk for vm in vms_list]
        )


@register_model_view(Project, 'add_virtualmachine', path='virtualmachine/add')
class ProjectAddInstanceView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectAddInstanceForm
    template_name = 'project_views/project_add_virtualmachine.html'

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
            vm_pks = form.cleaned_data['virtualmachine']
            with transaction.atomic():
                # Assign the selected VM to the Project
                for virtualmachine in VirtualMachine.objects.filter(pk__in=vm_pks):
                    project.virtualmachine.add(virtualmachine)
                    project.save()
            messages.success(request, "Added {} VirtualMachine to Project {}".format(
                len(vm_pks), project
            ))
            return redirect(project.get_absolute_url())

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': project.get_absolute_url(),
        })

