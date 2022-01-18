# PortalDjango

To run the project for the first time:

```
pip install -r requirements.txt
```
This will install the depedencies required to run the project. 

Then run the following commands in succession:
```
python manage.py makemigrations
python manage.py migrate --run-syncdb
```
These will create the database required for the project.
Then create a superuser with following command:
```
python manage.py createsuperuser
```
Use an appropriate user email and password. 
Now run the server:
```
python manage.py runserver
```

Then login to this link with the created superuser account:
```
<localhost>/admin/
```
Navigate to Users table. Create a new superadmin account. After account creation, click on the new user and check on is_superadmin. Then you can log out from superuser account and again log back in using the new superadmin account.