from modules.SearchSystem import find_most_similar
from flask import Flask, render_template, request, redirect, url_for, Response
from modules.admin import AdminPanel, Products, defence
from config import *

admin = AdminPanel()


@app.route("/")
def index():
    if defence.parsing_defence(request):
        return render_template("index.html")
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
def cart():
    if defence.parsing_defence(request):
        return "Cart page"
    return Response(status=403)


@app.route('/login')
def login():
    if defence.parsing_defence(request):
        return "Login page"
    return Response(status=403)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        products = Products.query.all()
    app.run(debug=True)
