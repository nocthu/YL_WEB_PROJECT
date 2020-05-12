# encoding: utf-8
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    sex = RadioField('Пол', choices=[('М', 'М'), ('Ж', 'Ж')])
    weight = StringField('Вес')
    submit = SubmitField('Зарегистрироваться')





