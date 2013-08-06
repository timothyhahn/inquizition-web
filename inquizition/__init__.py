from flask import Flask

app = Flask(__name__,static_url_path="/app", static_folder="app")



import inquizition.views
