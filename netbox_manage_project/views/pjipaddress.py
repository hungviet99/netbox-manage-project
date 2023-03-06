from netbox.views import generic
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Project
from .. import forms, tables
from django.db import transaction
from ipam.models import IPAddress
from ipam.tables import IPAddressTable
from ipam.filtersets import IPAddressFilterSet
from django.urls import reverse
from django.utils.translation import gettext as _
from utilities.views import ViewTab, register_model_view
from django.contrib import messages


@register_model_view(Project, 'ipaddress')
class ProjectIPAddressView(generic.ObjectChildrenView):
    queryset = Project.objects.all()
    child_model = IPAddress
    table = IPAddressTable
    filterset = IPAddressFilterSet
    template_name = 'project_views/ipaddress.html'
    tab = ViewTab(
        label=_('IPAddress'),
        badge=lambda obj: obj.ipaddress.count() if obj.ipaddress else 0,
        weight=600
    )
     # permission='virtualization.view_virtualmachine',
    def get_children(self, request, parent):
        return IPAddress.objects.restrict(request.user, 'view').filter(
            custom_field_data__project='project_{}'.format(parent.pk)
        )



@register_model_view(Project, 'add_ipaddress', path='ipaddress/add')
class ProjectAddIPAddressView(generic.ObjectEditView):
    queryset = Project.objects.all()
    form = forms.ProjectAddIPAddressForm
    template_name = 'project_views/project_add_ipaddress.html'

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
            ipaddress_pks = form.cleaned_data['ipaddress']
            with transaction.atomic():

                # Assign the selected IPAddress to the Project
                for ipaddress in IPAddress.objects.filter(pk__in=ipaddress_pks):
                    custom_field_data = ipaddress.custom_field_data
                    custom_field_data['project'] = 'project_{}'.format(pk)
                    ipaddress.custom_field_data = custom_field_data
                    ipaddress.save()

            messages.success(request, "Added {} ipaddress to project {}".format(
                len(ipaddress_pks), project
            ))
            return redirect(project.get_absolute_url())

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': project.get_absolute_url(),
        })

