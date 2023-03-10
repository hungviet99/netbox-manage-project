# Netbox Manage Project

## Installing

Để cài đặt plugin, trước tiên cần clone source code về máy. Sử dụng phương thức ssh để clone:

```
mkdir -p /opt/netbox/plugins && cd /opt/netbox/plugins
git clone git@github.com:hungviet99/netbox-manage-project.git
```

Sau khi clone source code về local, thực hiện install plugin. 

```
cd /opt/netbox/plugins/netbox-manage-project
python3 setup.py develop
```

Tiếp theo thực hiện enable plugin trong `/opt/netbox/netbox/netbox/configuration.py`, hoặc nếu có file `/configuration/plugins.py` thì file `plugin.py` sẽ được ưu tiên. 

```
PLUGINS = [
    'netbox_manage_project'
]
```

Khi đã enable plugin, cần thực hiện migrate db:

```
cd /opt/netbox/netbox/
python3 manage.py migrate
```

Sau đó có thể cần thực hiện bước cuối cùng là restart lại service để đảm bảo các thay đổi diễn ra được chính xác:

```
sudo systemctl restart netbox
```
