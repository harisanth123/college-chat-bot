from re import DEBUG
from flask import Flask, render_template,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from nltk import text
from werkzeug.wrappers import response
from chat import get_response
from flask_login import UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://database.db'
app.config['SECRET_KEY']='chatbot'



@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response= get_response(text)
    message={"answer":response}
    return jsonify(message)
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__=="__main__":
    app.run(debug=True)