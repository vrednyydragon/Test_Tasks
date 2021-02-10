# The Test Task 

####How to run on Ubuntu:

- Install Python and etc if needed
- git clone *Alias_test*
- In a terminal window, navigate into *Alias_test* directory where manage.py is located.
- This Django application is ready to use. By default, Django doesn’t allow external hosts to access the web interface. 
  To allow external hosts, edit settings.py file and add IP under ALLOWED_HOSTS. ***vim Alias_test/settings.py***
- Add the IP:
  
    ***ALLOWED_HOSTS = ['your_server_IP']*** 
  
    Note : Change your_server_IP details with your actual server IP as xx.xx.xx.xx

- Finally, run the Django application server with below command ***python3 manage.py runserver 0.0.0.0:8000***
- Django application server is running now. Open your web browser and access the Django Application with your server IP
  on port 8000. This will show you the Django web page.

- Run application tests ***python3 manage.py test***

## commands for install/check Python and Django:
python3 -V

sudo apt-get install python3 

django-admin –version

sudo apt install python3-django

## Commands to run tests:

python3 manage.py test

## Commands to run application:

python3 manage.py runserver 0.0.0.0:8000
