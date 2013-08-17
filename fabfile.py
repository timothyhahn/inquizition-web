from fabric.api import *
from fabric.contrib.files import exists


env.user = 'inquizition'
env.hosts = ['inquizition.us']


def deploy():
    with cd('~/inquizition-web'):
        with prefix('source venv/bin/activate'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('python manage.py init_db')
            run('python manage.py load_db')
            if exists('gunicorn.pid'):
                run('kill $(cat gunicorn.pid)')
            run('python manage.py gunicorn')

    put('inquizition/app', '/var/www/')
