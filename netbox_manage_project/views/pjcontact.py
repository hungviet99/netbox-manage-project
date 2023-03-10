from netbox.views import generic
from .. import forms, models
from tenancy.models import Contact
from utilities.views import ViewTab, register_model_view
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import transaction


@register_model_view(models.Project, 'add_contact', path='contact/add')
class ProjectAddContactView(generic.ObjectEditView):
    queryset = models.Project.objects.all()
    form = forms.ProjectAddContactForm
    template_name = 'project_views/project_add_contact.html'

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

            contact_pks = form.cleaned_data['contact']
            with transaction.atomic():

                # Assign the selected Contact to the Project
                for contact in Contact.objects.filter(pk__in=contact_pks):
                    project.contact.add(contact)
                    project.save()

            messages.success(request, "Added {} contact to project {}".format(
                len(contact_pks), project
            ))
            return redirect(project.get_absolute_url())

        return render(request, self.template_name, {
            'project': project,
            'form': form,
            'return_url': project.get_absolute_url(),
        })