from netbox.views import generic
from .. import forms, models, tables


# User view
class UserView(generic.ObjectView):
    queryset = models.User.objects.all()

class UserListView(generic.ObjectListView):
    queryset = models.User.objects.all()
    table = tables.UserTable

class UserEditView(generic.ObjectEditView):
    queryset = models.User.objects.all()
    form = forms.UserForm

class UserDeleteView(generic.ObjectDeleteView):
    queryset = models.User.objects.all()