import os
import requests
import datetime

from flask import Flask, render_template, redirect, session, request
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from data import db_session
from data.users import User

from Constants import *
from DataBase import DataBaseUser, Advices, Cities
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
    if request.method == 'GET':
        if int(session.get('status', GUEST)) & READ:
            date = user.get(session['user_id'])[DATE]
            # print(date, datetime.date.today(), str(date) != str(datetime.date.today()))
            if str(date) != str(datetime.date.today()):
                percent = 0
                user.update_percent(session['user_id'], '0')
            else:
                percent = user.get(session['user_id'])[PERCENT]
            return render_template('water.html', percent=(str(percent)+'%'))
        return render_template('b_1.html')
    elif request.method == 'POST':
        if request.form['size'].isalpha():
            return render_template('water.html', message="Введите натуральное число")

        size = int(request.form['size'])
        drink = request.form['drink']
        percent = int(user.get(session['user_id'])[PERCENT])
        water = int(user.get(session['user_id'])[WATER])

        if drink == 'Напиток...':
            return render_template('water.html', message="Выберете напиток")
        elif drink in {"Вода", "Миниральная вода"}:
            # new_percent = 100 - round(((water * ((100 - percent) / 100) - size) * 100) / water)
            pass
        elif drink in {'Сок', 'Молоко'}:
            pass
        elif drink == "Чай":
            size *= -0.3
        elif drink == 'Сладкая газированная вода':
            pass
        elif drink == "Кофе":
            size *= -1.5
        elif drink == "Алкоголь":
            pass

        new_percent = 100 - round(((water * ((100 - percent) / 100) - size) * 100) / water)

        if new_percent > 100:
            new_percent = 100
        elif new_percent < 0:
            new_percent = 0

        user.update_percent(session['user_id'], str(new_percent))
        return redirect('/waterbalance')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    all = cities.get_all()
    weather_data = []
    for item in all:
        city = item[1]
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=eacbcd14d851ef4babf54d5073484017'
        r = requests.get(url.format(city)).json()
        weather = {
            'item_id': item[0],
            'city': city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(weather)
    return render_template('weather.html', weather_data=weather_data)


@app.route('/add_city', methods=['GET', 'POST'])
def add_city():
    if request.method == 'GET':
        return render_template('add_city.html')
    elif request.method == 'POST':
        city_name = request.form['city_name']
        if city_name:
            cities.insert(city_name)
            return redirect('/weather')
        return render_template('add_city.html', message="Все поля должны быть заполнены")


@app.route('/delete_city/<int:city_id>', methods=['GET'])
def delete_city(city_id):
    if 'user_name' not in session:
        return redirect('/login')
    cities.delete(city_id)
    return redirect("/weather")


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

    cities = Cities()
    cities.init_table()

    main()
