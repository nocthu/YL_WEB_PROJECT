from flask import Flask, render_template, redirect, session
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from data import db_session
from data.users import User

from Constants import *
from DataBase import DataBase, DataBaseUser
from Forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


@app.route('/')
def home():
    # print(session.get('status', 0))
    if int(session.get('status', GUEST)) & READ:
        print(1)

    return render_template('home.html')


@app.route('/home', methods=['GET', 'POST'])
def choose():
    return render_template('choose_service.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('r_1.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        vse = user.get_all()
        for i in vse:
            if i == form.email.data:
                return render_template('r_1.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")

        user.insert(form.email.data, form.name.data, form.password.data, form.sex.data, form.weight.data, USER)
        return redirect('/home')

    return render_template('r_1.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        exists = user.exists(email, password)
        if exists[0]:
            session['email'] = email
            session['status'] = user.get(exists[1])[STATUS]
            session['user_id'] = exists[1]
            return redirect('/home')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/some_note', methods=['GET', 'POST'])
def some_note():
    return render_template('some_note.html')


@app.route('/waterbalance', methods=['GET', 'POST'])
def waterbalance():
    if int(session.get('status', GUEST)) & READ:
        return render_template('waterbalance.html')
    return render_template('home.html')


@app.route('/places')
def places():
    if int(session.get('status', GUEST)) & READ:
        return render_template('places.html')
    return render_template('home.html')


@app.route('/weather')
def weather():
    if int(session.get('status', GUEST)) & READ:
        return render_template('weather.html')
    return render_template('home.html')

@app.route('/advices')
def advices():
    if int(session.get('status', GUEST)) & READ:
        return render_template('advices.html')
    return render_template('home.html')

if __name__ == '__main__':
    user = DataBaseUser()
    user.init_table()
    main()
