from flask import Flask
app = Flask(__name__)

app.secret_key = "This_is_a_secret"