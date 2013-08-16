from fabric.api import *


env.user = 'inquizition'
env.hosts = ['inquizition.us']


def deploy():
    with cd('~/inquizition-web'):
        with prefix('source venv/bin/activate'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('python manage.py init_db')
            run('python manage.py load_db')
            run('python manage.py gunicorn')

    put('inquizition/app', '/var/www/')
