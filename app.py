from enum import unique
from re import DEBUG
from flask import Flask, render_template,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import model
from flask_sqlalchemy.model import Model
from flask_wtf import form
from flask_wtf.form import FlaskForm
from nltk import text
from werkzeug.utils import redirect
from werkzeug.wrappers import response
from chat import get_response
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='chatbot'
db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4,max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(
        min=4,max=20)], render_kw={"placeholder":"password"})
    submit =SubmitField("Register")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That user alrady exist's. please choose a different one")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(
        min=4,max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(),Length(
        min=4,max=20)], render_kw={"placeholder":"password"})
    submit =SubmitField("Login")

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response= get_response(text)
    message={"answer":response}
    return jsonify(message)
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form =RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__=="__main__":
    app.run(debug=True)