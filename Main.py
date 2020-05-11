import os
import requests
import datetime

from flask import Flask, render_template, redirect, session, request
from flask_ngrok import run_with_ngrok
from Constants import *
from DataBase import DataBaseUser, Advices, Cities
from Forms import RegisterForm, LoginForm, NewsForm

from socket import gethostname

app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def choose():
    if int(session.get('status', GUEST)) & READ:
        return render_template('b_1.html', pic=str(user.get(session['user_id'])[USER_FILE]))
    return render_template('b_1.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if int(session.get('status', GUEST)) & READ:
        if request.method == 'GET':
            return render_template('profile.html', email=session['email'], user_name=session['user_name'],
                                   status=session['status'], photo=1)
        elif request.method == 'POST':
            new_user_name = request.form['user_name']
            if new_user_name != session['user_name']:
                user.update(session['user_id'], 'user_name', new_user_name)
                session['user_name'] = new_user_name
            if request.files.get('file', None):
                photo = 'static/user_files/' + request.files['file'].filename
                request.files['file'].save(photo)
                all = user.get(session['user_id'])
                os.remove(all[USER_FILE])
                user.update(session['user_id'], 'user_file', photo)
            return redirect("/profile")

    return redirect('/login')


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
            date = user.get(session['user_id'])[DATE]
            if datetime.date.today() != date:
                user.update(session['user_id'], 'percent', '0')
                user.update(session['user_id'], 'date', str(datetime.date.today()))
                user.update(session['user_id'], 'days_here', str(int(user.get(exists[1])[DAYS_HERE]) + 1))
                if int(user.get(exists[1])[DAYS_HERE]) > 30:
                    user.update(session['user_id'], 'status', MODERATOR)
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
                user.update(session['user_id'], 'percent', '0')
                user.update(session['user_id'], 'date', str(datetime.date.today()))
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
        elif drink in {'Фруктовый чай'}:
            size *= 0.9
        elif drink in {"Минеральная вода", "Чёрный чай", "Зелёный чай"}:
            size *= 0.8
        elif drink in {'Крепкий чёрный чай', 'Крепкий зелёный чай'}:
            size *= 0.7
        elif drink in {'Кофе'}:
            size *= 0.3
        elif drink in {'Кофе с молоком'}:
            size *= 0.2
        elif drink in {'Сок', 'Молоко', 'Какао', 'Морс', 'Компот', 'Кефир', 'Йогурт'}:
            size = 0
        elif drink in {'Айран'}:
            size *= -0.2
        elif drink in {'Молочный коктейль', 'Спортивный коктейль'}:
            size *= -0.3
        elif drink in {'Сладкая газированная вода', "Спортивный энергетик"}:
            size += -0.4
        elif drink in {'Пиво'}:
            size += -0.5
        elif drink in {'Белое сухое вино', "Красное сухое вино", 'Алкогольный коктейль'}:
            size += -0.6
        elif drink in {'Белое полусладкое вино', "Красное полусладкое вино", 'Энергетик'}:
            size += -0.8
        elif drink in {"Крепкий алкоголь"}:
            size *= -1.8

        new_percent = 100 - round(((water * ((100 - percent) / 100) - size) * 100) / water)

        user.update(session['user_id'], 'percent', str(new_percent))
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
        if user.get(session['user_id'])[POSTS] >= 3 and user.get(session['user_id'])[STATUS] == MODERATOR:
            return render_template('add_advice.html', message="У вас не хватает прав для добавления ещё одного совета")
        title = request.form['name']
        content = request.form['advice']
        if title and content and request.files.get('file', None):
            photo = 'static/images/' + request.files['file'].filename
            request.files['file'].save(photo)
            advices.insert(title, content, photo, session['user_id'])
            user.update(session['user_id'], 'posts', str(int(user.get(session['user_id'])[POSTS]) + 1))
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

    if 'liveconsole' not in gethostname():
        main()
