### Run command to create virtual environment and ensure packages' version are consistent
```
pyenv local 3.10.7 # this sets the local version of python to 3.7.0
python3 -m venv .venv # this creates the virtual environment for you
source .venv/bin/activate # this activates the virtual environment
pip install -r requirements.txt
pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
```

### Run command to initialise database
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # username:admin email:admin@gmail.com password:qwe147369
python manage.py parse_csv
```
### Run command to run server
```
python manage.py runserver
```