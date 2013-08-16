# Inquizition

> The webservice portion of our "Inquizition" application, a trivia quiz game with friends.

## Setup

* Install pip (http://www.pip-installer.org/en/latest/installing.html).

* Install virtualenv
```
[sudo] pip install virtualenv
```

* Create virtualenv
```
virtualenv venv
```

* Activate virtualenv
```
source venv/bin/activate
```

* Install requirements
```
pip install -r requirements.txt
```

* Initialize database
```
python manage.py init_db
python manage.py load_db
```

* Run development server
```
python manage.py runserver
```

## Other Things

* Run tests
```
python manage.py test
OR
python manage.py coverage
```

* Deploy
```
fab deploy
```

## API
API description is at is at https://github.com/timothyhahn/inquizition-web/wiki/API
