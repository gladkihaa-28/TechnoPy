from modules.SearchSystem import find_most_similar
from flask import Flask, render_template, request, redirect, url_for, Response, flash, make_response
from modules.admin import AdminPanel, Products, defence
from UserLogin import UserLogin, get_user, get_user_name, get_user_psw, get_user_by_name, update_user_avatar, update_user_cart, get_user_cart, clear_user_cart
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import *
import sqlite3
import time

admin = AdminPanel()

login_manager = LoginManager(app)
con = sqlite3.connect("instance/products.db")
cur = con.cursor()
result = cur.execute("""SELECT COUNT(*) FROM products""").fetchall()
for elem in result:
    print(elem)
con.close()
con = sqlite3.connect("instance/users.db")
cur = con.cursor()
res2 = cur.execute("""SELECT COUNT(*) FROM users""").fetchall()
res2 = str(res2)[2]
print(res2)
con.close()


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().from_db(user_id)


@app.route("/")
def index():
    if defence.parsing_defence(request):
        products = Products.query.all()
        lust_products = []
        all_products = [el for el in products if el.id <= 5]
        for i in range(len(all_products[:4])):
            lust_products.append(all_products[-(i + 1)])
        return render_template("index.html", products=lust_products)
    return Response(status=403)


@app.route("/catalog")
def catalog():
    if defence.parsing_defence(request):
        products = Products.query.all()
        return render_template("catalog.html", products=products)
    return Response(status=403)

@app.route("/product/<name>")
def product(name):
    if defence.parsing_defence(request):
        products = Products.query.all()
        card = [el for el in products if el.name == name][0]
        return render_template("card.html", product=card)
    return Response(status=403)

@app.route("/add_card/<name>", methods=["GET", "POST"])
def add_card(name):
    if request.method == "POST":
        id = None
        for i, el in enumerate(products):
            if el.name == name:
                id = i + 1
                break
        card = [el for el in products if el.name == name][0]
        user_id = current_user.get_id()
        update_user_cart(id, user_id)
        return render_template("card.html", product=card)

@app.route("/smartphones")
def smartphones():
    if defence.parsing_defence(request):
        products = [product for product in Products.query.all() if product.category.lower() == "смартфон"]
        return render_template("catalog.html", products=products)
    return Response(status=403)

@app.route("/tablets")
def tablets():
    if defence.parsing_defence(request):
        products = [product for product in Products.query.all() if product.category.lower() == "планшет"]
        return render_template("catalog.html", products=products)
    return Response(status=403)

@app.route("/laptops")
def laptops():
    if defence.parsing_defence(request):
        products = [product for product in Products.query.all() if product.category.lower() == "ноутбук"]
        return render_template("catalog.html", products=products)
    return Response(status=403)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if defence.parsing_defence(request):
        products = Products.query.all()
        if request.method == 'POST':
            text = str(request.form.get('text'))
            if len(set(text)) != 1:
                sp = find_most_similar(text, [product.name for product in products])
                print(sp)
                search_products = [product for product in products if product.name in sp]
                return render_template("catalog.html", products=search_products)
            else:
                return render_template("catalog.html", products=products)
        return render_template("catalog.html", products=products)
    return Response(status=403)


@app.route('/cart')
@login_required
def cart():
    if defence.parsing_defence(request):
        user_id = current_user.get_id()
        products = get_user_cart(user_id)
        lust_products = [card for card in Products.query.all() if card.id in  products]
        return render_template("cart.html", products=lust_products)
    return Response(status=403)


@app.route('/clear_cart')
@login_required
def clear_cart():
    if defence.parsing_defence(request):
        user_id = current_user.get_id()
        clear_user_cart(user_id)
        return render_template("cart.html", products=[])
    return Response(status=403)

@app.route("/login", methods=["POST", "GET"])
def login():
    if defence.parsing_defence(request):
        if request.method == "POST":
            user = get_user_by_name(request.form['name'])
            if user and (str(get_user_psw(request.form['name'])) == str(request.form['psw'])):
                user_login = UserLogin().create(user)
                print(user_login)
                login_user(user_login)
                flash("Вы успешно вошли", "success")
                return redirect(url_for("profile"))

            flash("Неверный логин/пароль", "error")

        return render_template("login.html")
    return Response(status=403)


@app.route("/register", methods=["POST", "GET"])
def register():
    if defence.parsing_defence(request):
        if request.method == "POST":
            if len(request.form['name']) > 4 and len(request.form['psw']) > 4 \
                    and request.form['psw'] == request.form['psw2']:
                id = int(res2) + 1
                name = str(request.form['name'])
                psw = str(request.form['psw'])
                if get_user_name(name) == False:
                    flash("Имя занято", 'error')
                else:
                    con = sqlite3.connect("instance/users.db")
                    cur = con.cursor()
                    res = cur.execute('INSERT INTO Users (id, name, psw, cart, avatar) VALUES (?, ?, ?, NULL, NULL)', (id, name, psw))
                    con.commit()
                    con.close()
                    if res:
                        flash("Вы успешно зарегистрированы", "success")
                        return redirect(url_for('login'))
                    else:
                        flash("Ошибка при добавлении в БД", "error")
            else:
                flash("Неверно заполнены поля", "error")
        return render_template("register.html")
    return Response(status=403)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_avatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verify_ext(file.filename):
            try:
                img = file.read()
                user_id = current_user.get_id()
                res = update_user_avatar(img, user_id)
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")

    return redirect(url_for('profile'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        products = Products.query.all()
    app.run(debug=True)
