import os

from flask import Flask, render_template, redirect, session, request
import requests
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
        return render_template('b_1.html')
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
        return render_template('water.html')
    return render_template('b_1.html')


@app.route('/places')
def places():
    if int(session.get('status', GUEST)) & READ:
        return render_template('places.html')
    return render_template('b_1.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    # if int(session.get('status', GUEST)) & READ:
    #     city = 'Moscow'
    #     if request.method == 'POST':
    #         city = request.form.get('city')
    #     if city is not None:
    #         url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=eacbcd14d851ef4babf54d5073484017'
    #         appid = 'eacbcd14d851ef4babf54d5073484017'
    #         city_id = 0
    #         r = requests.get(url.format(city)).json()
    #         res = requests.get("http://api.openweathermap.org/data/2.5/weather",
    #                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    #         weather = {
    #             'city': city,
    #             'temperature': r['main']['temp'],
    #             'description': r['weather'][0]['description'],
    #             'icon': r['weather'][0]['icon']
    #         }
    #         return render_template('weather.html', weather=weather)
    # return render_template('b_1.html')


    city = None
    if request.method == 'POST':
        # city = request.form.get('city_name')
        city = request.form['city_name']
        print(city)
    if request.method == 'GET':
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=eacbcd14d851ef4babf54d5073484017'
        r = requests.get(url.format(city)).json()
        print(r)
        weather = {
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        print(weather)
        return render_template('weather.html', weather=weather)


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
        if title and content and request.files.get('file', None):
            photo = 'static/images/' + request.files['file'].filename
            request.files['file'].save(photo)
            advices.insert(title, content, photo, session['user_id'])
            return redirect("/advices")
        return render_template('add_advice.html', message="Все поля должны быть заполнены")


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
