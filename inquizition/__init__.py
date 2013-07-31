from flask import Flask, url_for, redirect, request, render_template
from database import db_session
from models import Quiz

app = Flask(__name__)

## RUN APPLICATION
if __name__ == '__main__':
    app.run(host='0.0.0.0')
