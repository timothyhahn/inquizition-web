from flask.ext.script import Manager
from inquizition import app

manager = Manager(app)

@manager.command
def gunicorn():
    "Runs this with gunicorn (Production server)"
    import subprocess
    subprocess.call(['./scripts/gunicorn.sh'])

@manager.command
def init_db():
    "Sets up the DB"
    print "Setting up DB"
    from inquizition.database import init_db
    init_db()


if __name__ == "__main__":
    manager.run()
