steps to follow-
Clone repository

Create Virtualenv Command - virtualenv YOUR_VIRTUAL_ENV_NAME

Activate virtual environment -in Power Shell- YOUR_VIRTUAL_ENV_NAME\Scripts\activate

install all packages and dependencies at once from requirements.txt Command (In virtual environment): pip install -r requirements.txt NOTE: This Command will install all the supporting packages listed in requirements.txt files

Create Super User to access admin panel (In virtual environment)- python manage.py createsuperuser
Run Migrations 
1. makemigrations:To create inital table or database files in database run command in vertual environment-: python manage.py makemigrations 
2. migrate : To migrate the changes run command in vertual environment- python manage.py migrate

Run Server Command Prompt (In virtual environment): python manage.py runserver
