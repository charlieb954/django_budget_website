# django_budget_website

### django notes
    - django-admin startproject <site name> -> creates a variety of files for your project
    - python3 manage.py runserver -> to run the project
    - python3 manage.py migrate -> creates neccessary database tables
    - python3 manage.py makemigrations -> store the changes made as a migration

### How to run the django application
1. git clone <this repo url>
2. pip install -r requirements.txt
3. python3 -m venv venv/ 
    - Creates an environment called venv/ you can replace “venv/” with a different name for your environment
4. activate the virtual envrionment
    - source venv/bin/activate
5. cd into the cloned folder
6. python3 manage.py runserver
