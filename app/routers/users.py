from flask import Blueprint, render_template, request
from models import User
from sqlalchemy import insert, select
from backend.db import db

user_router = Blueprint('user_router', __name__)


@user_router.get("/registration")
def registration():
    return render_template(template_name_or_list='personality/registration.html', context={})


@user_router.post("/registration_info")
def registration_info():
    """
    function that is triggered
    when the "confirm" button is clicked on a registration page
    and verifies the data entered by the user
    :return: page template and message about the result of data verification
    """
    context = {}
    username = request.form['username']
    password = request.form['password']
    repeat_password = request.form['repeat_password']
    email = request.form['email']
    phone = request.form['phone']
    birthday = request.form['birthday']

    user_find = db.scalar(select(User).where(User.username == username))
    if len(username) > 20 or len(password) < 8 or len(phone) > 12 or len(birthday) > 10:
        context['message'] = 'Неверный формат данных!'
        return render_template(template_name_or_list='personality/registration.html', context=context)
    if user_find:
        context['message'] = 'Такой пользователь уже существует!'
        return render_template(template_name_or_list='personality/registration.html', context=context)
    if password != repeat_password:
        context['message'] = 'Пароли не совпадают!'
        return render_template(template_name_or_list='personality/registration.html', context=context)

    db.execute(insert(User).values(username=username,
                                   password=password,
                                   email=email,
                                   phone=phone,
                                   birthday=birthday))
    db.commit()
    context['message'] = 'Вы успешно зарегистрированы!'
    return render_template(template_name_or_list='personality/registration.html', context=context)


@user_router.get("/login")
def login():
    return render_template(template_name_or_list='personality/login.html', context={})


@user_router.post("/login_info")
def login_info():
    """
    function that is triggered
    when the "confirm" button is clicked on a login page
    and verifies the data entered by the user
    :return: page template and message about the result of data verification
    """
    context = {}
    username = request.form['username']
    password = request.form['password']

    user_find = db.scalar(select(User).where(User.username == username))
    if not user_find:
        context['message'] = 'Такой пользователь не зарегистрирован!'
        return render_template(template_name_or_list='personality/login.html', context=context)
    if password != user_find.password:
        context['message'] = 'Пароли не совпадают!'
        return render_template(template_name_or_list='personality/login.html', context=context)

    context = {
        'username': user_find.username,
        'email': user_find.email,
        'phone': user_find.phone,
        'birthday': user_find.birthday
    }
    return render_template(template_name_or_list='personality/profil.html', context=context)
