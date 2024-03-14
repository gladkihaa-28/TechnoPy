from flask import request, render_template, Response, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import *
from modules.server_defence import Defence

defence = Defence()


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    parameters = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)


def AdminPanel():
    admin = Admin(app)
    admin.add_view(ModelView(Products, db.session))
    return admin


@app.route('/login_admin')
def admin():
    if defence.parsing_defence(request):
        return render_template("admin.html")
    return Response(status=403)


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if defence.parsing_defence(request):
        if request.method == 'POST':
            login = request.form.get("login")
            password = request.form.get("password")
            if login == "Thread554" and password == "A280811g":
                return redirect(url_for('admin.index'))
        return redirect('/')
    return Response(status=403)