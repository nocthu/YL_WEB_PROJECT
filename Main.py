import os

from flask import Flask, render_template, redirect, session, request
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from data import db_session
from data.users import User

from Constants import *
from DataBase import DataBaseUser, Advices
from Forms import RegisterForm, LoginForm, NewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


@app.route('/')
def home():
    # print(session.get('status', 0))
    if int(session.get('status', GUEST)) & READ:
        return render_template('home.html')
    return render_template('b_1.html')


@app.route('/home', methods=['GET', 'POST'])
def choose():
    return render_template('b_1.html')


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
            session['user_name'] = user.get(exists[1])[USERNAME]
            session['status'] = user.get(exists[1])[STATUS]
            session['user_id'] = exists[1]
            return redirect('/home')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('user_name', 0)
    session.pop('status', 0)
    session.pop('user_id', 0)
    return redirect('/')


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
def advice():
    all = advices.get_all()
    return render_template('advices.html',
                           advices=all,
                           write=(int(session.get('status', GUEST)) & WRITE),
                           execute=(int(session.get('status', GUEST)) & EXECUTE))


@app.route('/add_advice', methods=['GET', 'POST'])
def add_advice():
    if request.method == 'GET':
        return render_template('add_advice.html')
    elif request.method == 'POST':
        if 'user_name' not in session:
            return redirect('/login')
        title = request.form['name']
        content = request.form['advice']
        if title != '' and content != '':
            if request.files.get('file', None):
                photo = 'static/images/' + request.files['file'].filename
                request.files['file'].save(photo)
            else:
                return render_template('not_enough.html')
            advices.insert(title, content, photo, session['user_id'])
            return redirect("/advices")
        return render_template('not_enough.html')


@app.route('/delete_advice/<int:news_id>', methods=['GET'])
def delete_book(news_id):
    if 'user_name' not in session:
        return redirect('/login')
    all = advices.get(news_id)
    os.remove(all[FILE])
    advices.delete(news_id)
    return redirect("/advices")


if __name__ == '__main__':

    user = DataBaseUser()
    user.init_table()

    advices = Advices()
    advices.init_table()

    main()
