# ToDo

Setting up the local environment

To set up the local environment for this Django project, you will need to install Python and a virtual environment manager.

If you are using Python 3.6 or higher, you can use the built-in virtual environment manager:
python -m venv venv

If you are using an older version of Python, you can use a third-party virtual environment manager, such as virtualenv:
pip install virtualenv
virtualenv venv

Once you have created a virtual environment, you can activate it:
source venv/bin/activate

now install the required dependencies for this Django project:
pip install -r requirements.txt

this project is using mysql. if you are not intrested in using mysql change the database setting in sttings.py

for setting the database info, create a database:
CREATE DATABASE task_manager

then pass the necessary information for it in settings.py

then migrate the database:
python manage.py migrate

Finally, you can create a superuser account:
python manage.py createsuperuser

To run the project, simply run the following command:

python manage.py runserver

This will start the development server on port 8000. You can now access the project in web browser at http://localhost:8000.
