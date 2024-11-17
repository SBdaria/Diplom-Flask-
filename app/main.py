from flask import Flask, render_template, request
from routers.users import user_router
from backend.db import db
from sqlalchemy import insert, select
from models import Product, User, Cart
from datetime import datetime

app = Flask(__name__)
app.register_blueprint(user_router)


@app.get('/')
def homepage():
    context = {'namepage': 'homepage', 'title': 'Главная страница'}
    return render_template(template_name_or_list='mainpages/homepage.html', context=context)


@app.get('/catalog')
def catalog():
    context = {'namepage': 'catalog', 'title': 'Каталог'}
    return render_template(template_name_or_list='mainpages/catalog.html', context=context)


@app.get('/about')
def about():
    context = {'namepage': 'about', 'title': 'О нас'}
    return render_template(template_name_or_list='mainpages/about_us.html', context=context)


@app.get('/info')
def info():
    context = {'namepage': 'info', 'title': 'Доставка и оплата'}
    return render_template(template_name_or_list='mainpages/info.html', context=context)


@app.get('/jackets')
def jackets():
    jackets = db.query(Product).filter(Product.category == 'jackets').all()
    context = {'namepage': 'jackets', 'category': 'Куртки', 'type_cloth': jackets}
    return render_template(template_name_or_list='mainpages/catalogpage.html', context=context)


@app.get('/tshirts')
def tshirts():
    tshirts = db.query(Product).filter(Product.category == 'tshirts').all()
    context = {'namepage': 'tshirts', 'category': 'Футболки', 'type_cloth': tshirts}
    return render_template(template_name_or_list='mainpages/catalogpage.html', context=context)


@app.get('/hoodies')
def hoodies():
    hoodies = db.query(Product).filter(Product.category == 'hoodies').all()
    context = {'namepage': 'hoodies', 'category': 'Худи', 'type_cloth': hoodies}
    return render_template(template_name_or_list='mainpages/catalogpage.html', context=context)


@app.get('/jeans')
def jeans():
    jeans = db.query(Product).filter(Product.category == 'jeans').all()
    context = {'namepage': 'jeans', 'category': 'Джинсы', 'type_cloth': jeans}
    return render_template(template_name_or_list='mainpages/catalogpage.html', context=context)


@app.get('/shoes')
def shoes():
    shoes = db.query(Product).filter(Product.category == 'shoes').all()
    context = {'namepage': 'shoes', 'category': 'Кроссовки и кеды', 'type_cloth': shoes}
    return render_template(template_name_or_list='mainpages/catalogpage.html', context=context)


@app.get('/cart/<cloth_id>')
def cart_info(cloth_id: int):
    cloth = db.scalar(select(Product).where(Product.id == cloth_id))
    context = {'namepage': 'shoes', 'title': 'Подтверждение заказа', 'cloth': cloth}
    return render_template(template_name_or_list='mainpages/cart_info.html', context=context)


@app.post("/cart_info/<cloth_id>")
def cart_order(cloth_id: int):
    """
    function that is triggered
    when the "confirm" button is clicked on a cart_info page
    and verifies the data entered by the user
    :param cloth_id: id of the product that the user selected
    :return: page template and message about the result of data verification
    """
    username = request.form['username']
    password = request.form['password']

    cloth = db.scalar(select(Product).where(Product.id == cloth_id))
    context = {'cloth': cloth}
    user_find = db.scalar(select(User).where(User.username == username))
    if not user_find:
        context.update({
            'namepage': 'shoes',
            'title': 'Подтверждение заказа',
            'message': 'Такой пользователь не зарегистрирован!'
        })
        return render_template(template_name_or_list='mainpages/cart_info.html', context=context)

    if password != user_find.password:
        context.update({
            'namepage': 'shoes',
            'title': 'Подтверждение заказа',
            'message': 'Пароли не совпадают!'
        })
        return render_template(template_name_or_list='mainpages/cart_info.html', context=context)
    db.execute(insert(Cart).values(date_order=datetime.now().strftime('%Y-%m-%d %H:%M'),
                                   user_id=user_find.id,
                                   product_id=cloth_id))
    db.commit()
    context.update({
        'namepage': 'submit_order',
        'title': 'Ваш заказ успешно подтвержден'
    })
    return render_template(template_name_or_list='mainpages/submit_order.html', context=context)


if __name__ == "__main__":
    app.run(debug=True)
