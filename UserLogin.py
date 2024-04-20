import time
import math
import re
from modules.SearchSystem import find_most_similar
from flask import Flask, render_template, request, redirect, url_for, Response, flash
from modules.admin import AdminPanel, Products, defence
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, UserMixin
from config import *
import sqlite3
import time


class UserLogin(UserMixin):
    def from_db(self, user_id):
        self.__user = get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

    def get_name(self):
        return self.__user[1] if self.__user else 'Без имени'

    def get_psw(self):
        return self.__user[2] if self.__user else "Без пароля"

    def get_avatar(self, app):
        img = None
        if not self.__user[4]:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='user_images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.__user[4]

        return img

    def verify_ext(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False



def get_user(user_id):
    try:
        con = sqlite3.connect("instance/users.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1").fetchone()
        if not res:
            print("Пользователь не найден")
            return False

        return res
    except sqlite3.Error as e:
        print("Ошибка получения данных из БД " + str(e))

    return False


def get_user_by_name(name):
    try:
        con = sqlite3.connect("instance/users.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM users WHERE name = '{name}' LIMIT 1")
        res = cur.fetchone()
        if not res:
            print("Пользователь не найден")
            return False

        return res
    except sqlite3.Error as e:
        print("Ошибка получения данных из БД " + str(e))

    return False


def get_user_name(name):
    con = sqlite3.connect("instance/users.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT COUNT(*) FROM users WHERE name = '{name}'")
    print(res)
    el = ''
    for el in res:
        print(el)
    ner = []
    ner.append(el[0])
    print(ner[0])

    if ner[0] == 0 or ner[0] == '0':
        con.close()
        return True
    con.close()
    return False


def get_user_psw(name):
    con = sqlite3.connect("instance/users.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT psw FROM users WHERE name = '{name}'").fetchone()
    return res[0]


def update_user_avatar(avatar, user_id):
    if not avatar:
        return False

    try:
        con = sqlite3.connect("instance/users.db")
        cur = con.cursor()
        binary = sqlite3.Binary(avatar)
        cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
        con.commit()
    except sqlite3.Error as e:
        print("Ошибка обновления аватара в БД: " + str(e))
        return False
    return True

def update_user_cart(id, user_id):
    try:
        con = sqlite3.connect("instance/users.db")
        cur = con.cursor()
        cards = cur.execute(f"SELECT cart FROM users WHERE id = '{user_id}'").fetchone()[0]
        try:
            cards.split(", ").remove("")
        except:
            pass
        if cards is None and cards == '':
            cards = []
        else:
            try:
                cards = cards.split(", ")
            except:
                cards = []
        try:
            cards = list(map(int, cards))
        except:
            cards.remove("")
        cards.append(id)
        cards = str(cards)[1:-1]
        cur.execute(f"UPDATE users SET cart = ? WHERE id = ?", (cards, user_id))
        con.commit()
    except sqlite3.Error as e:
        print("Ошибка обновления товара в БД: " + str(e))
        return False
    return True


def get_user_cart(user_id):
    try:
        con = sqlite3.connect("instance/users.db")
        cur = con.cursor()
        cards = cur.execute(f"SELECT cart FROM users WHERE id = '{user_id}'").fetchone()[0]
        try:
            cards.split(", ").remove("")
        except:
            pass
        if cards is None and cards == '':
            cards = []
        else:
            try:
                cards = cards.split(", ")
            except:
                cards = []
        cards = list(map(int, cards))
        con.close()
    except sqlite3.Error as e:
        print("Ошибка обновления товара в БД: " + str(e))
        return False
    return cards


def clear_user_cart(user_id):
    try:
        con = sqlite3.connect("instance/users.db")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET cart = ? WHERE id = ?", ("", user_id))
        con.commit()
    except sqlite3.Error as e:
        print("Ошибка обновления товара в БД: " + str(e))
        return False
    return True