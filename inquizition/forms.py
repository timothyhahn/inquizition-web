from flask.ext.wtf import Form, TextField, PasswordField, validators
from models import User
from database import db_session



class LoginForm(Form):
    username = TextField('Username', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        self.user = user
        return True

class RegisterForm(Form):
    username = TextField('Username', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
    
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            self.username.errors.append('Username already exists!')
            return False

        user = User(username=self.username.data)
        db_session.add(user)
        db_session.commit()
        self.user = user
        return True

