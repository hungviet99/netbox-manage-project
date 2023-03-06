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
    path('project/<int:pk>/instance/', views.ProjectInstanceView.as_view(), name='project_instance'),
    path('projects/<int:pk>/instance/add/', views.ProjectAddInstanceView.as_view(), name='project_add_instance'),
    # path('projects/<int:pk>/instance/remove/', views.ProjectRemoveInstanceView.as_view(), name='project_remove_instance'),

    # Quota Template
    path('quotatemplate/', views.QuotaTemplateListView.as_view(), name='quotatemplate_list'),
    path('quotatemplate/add/', views.QuotaTemplateEditView.as_view(), name='quotatemplate_add'),
    path('quotatemplate/<int:pk>/', views.QuotaTemplateView.as_view(), name='quotatemplate'),
    path('quotatemplate/<int:pk>/edit/', views.QuotaTemplateEditView.as_view(), name='quotatemplate_edit'),
    path('quotatemplate/<int:pk>/delete/', views.QuotaTemplateDeleteView.as_view(), name='quotatemplate_delete'),
    path('quotatemplate/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='quotatemplate_changelog', kwargs={
        'model': models.QuotaTemplate
    }),


    # User
    path('user/', views.UserListView.as_view(), name='user_list'),
    path('user/add/', views.UserEditView.as_view(), name='user_add'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    path('user/<int:pk>/edit/', views.UserEditView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('user/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='user_changelog', kwargs={
        'model': models.User
    }),

    # path('', include('netbox.api.urls')),
    # path('plugins/', include('plugins.api.urls', namespace='plugins-api')),
    # path('plugins/netbox_manage_project/', include('netbox_manage_project.urls', namespace='netbox_manage_project-api')),
)