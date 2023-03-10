from django.urls import path, include

from netbox.views.generic import ObjectChangeLogView
from . import models, views

urlpatterns = (

    # Project lists
    path('project/', views.ProjectListView.as_view(), name='project_list'),
    path('project/add/', views.ProjectEditView.as_view(), name='project_add'),
    path('project/<int:pk>/', views.ProjectView.as_view(), name='project'),
    path('project/<int:pk>/edit/', views.ProjectEditView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='project_changelog', kwargs={
        'model': models.Project
    }),
    # Project device
    path('project/<int:pk>/devices/', views.ProjectDevicesView.as_view(), name='project_devices'),
    path('projects/<int:pk>/devices/add/', views.ProjectAddDevicesView.as_view(), name='project_add_devices'),
    path('projects/<int:pk>/devices/remove/', views.ProjectRemoveDevicesView.as_view(), name='project_remove_devices'),

    # # Project IPAddress
    path('project/<int:pk>/ipaddress/', views.ProjectIPAddressView.as_view(), name='project_ipaddress'),
    path('projects/<int:pk>/ipaddress/add/', views.ProjectAddIPAddressView.as_view(), name='project_add_ipaddress'),
    # path('projects/<int:pk>/ipaddress/remove/', views.ProjectRemoveIPAddressView.as_view(), name='project_remove_ipaddress'),

    # project Instance
    path('project/<int:pk>/virtualmachine/', views.ProjectInstanceView.as_view(), name='project_virtualmachine'),
    path('projects/<int:pk>/virtualmachine/add/', views.ProjectAddInstanceView.as_view(), name='project_add_virtualmachine'),
    # path('projects/<int:pk>/virtualmachine/remove/', views.ProjectRemoveInstanceView.as_view(), name='project_remove_virtualmachine'),

    # Project Contact
    path('projects/<int:pk>/contact/add/', views.ProjectAddContactView.as_view(), name='project_add_contact'),

    # Quota Template
    path('quotatemplate/', views.QuotaTemplateListView.as_view(), name='quotatemplate_list'),
    path('quotatemplate/add/', views.QuotaTemplateEditView.as_view(), name='quotatemplate_add'),
    path('quotatemplate/<int:pk>/', views.QuotaTemplateView.as_view(), name='quotatemplate'),
    path('quotatemplate/<int:pk>/edit/', views.QuotaTemplateEditView.as_view(), name='quotatemplate_edit'),
    path('quotatemplate/<int:pk>/delete/', views.QuotaTemplateDeleteView.as_view(), name='quotatemplate_delete'),
    path('quotatemplate/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='quotatemplate_changelog', kwargs={
        'model': models.QuotaTemplate
    }),

)