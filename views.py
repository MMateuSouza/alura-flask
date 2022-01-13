from flask import flash, render_template, redirect, request, send_from_directory, session, url_for

from app import app, db
from helpers import has_signed_user, retrieve_image, delete_image
from models import Game
from dao import GameDAO, UserDAO

import time


game_dao = GameDAO(db)
user_dao = UserDAO(db)

@app.route("/")
@app.route("/games/")
def index():
    if not has_signed_user():
        return redirect(url_for("login", next=url_for("index")))
    games = game_dao.list()
    return render_template("games/list.html", title="Jogoteca", games=games)

@app.route("/games/register/")
def register():
    if not has_signed_user():
        return redirect(url_for("login", next=url_for("register")))
    return render_template("games/register.html", title="Novo Jogo")

@app.route("/games/create/", methods=["POST",])
def create():
    name = request.form["name"]
    category = request.form["category"]
    console = request.form["console"]
    game = Game(name=name, category=category, console=console)
    game_dao.save(game)

    file = request.files["file"]
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    file.save(f"{upload_path}/front_cover_{game.pk}-{timestamp}.jpg")

    return redirect(url_for("index"))

@app.route("/games/change/<int:pk>")
def change(pk):
    if not has_signed_user():
        return redirect(url_for("login", next=url_for("change")))
    game = game_dao.query_by_pk(pk=pk)
    front_cover = retrieve_image(game.pk)
    return render_template("games/change.html", title="Atualizar Jogo", game=game, front_cover=front_cover)

@app.route("/games/update/", methods=["POST",])
def update():
    pk = request.form["pk"]
    name = request.form["name"]
    category = request.form["category"]
    console = request.form["console"]
    game = Game(name=name, category=category, console=console, pk=pk)
    game_dao.save(game)

    file = request.files["file"]
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    delete_image(pk)
    file.save(f"{upload_path}/front_cover_{game.pk}-{timestamp}.jpg")

    return redirect(url_for("index"))

@app.route("/games/delete/<int:pk>")
def delete(pk):
    game_dao.delete(pk=pk)
    delete_image(pk)
    flash("Jogo excluído com sucesso!")
    return redirect(url_for("index"))

@app.route("/uploads/<filename>")
def image(filename):
    return send_from_directory("uploads", filename)

@app.route("/login/")
def login():
    next = request.args.get("next")
    return render_template("login.html", next=next)

@app.route("/authenticate/", methods=["POST",])
def authenticate():
    username = request.form["username"]
    password = request.form["password"]
    next = request.form["next"]
    user = user_dao.query_by_username(username=username)
    if user and password == user.password:
        session["signed_user"] = username
        flash(f"{username} autenticado com sucesso!")
        return redirect(next)
    flash(f"Usuário e/ou senha incorretos!")
    return redirect(url_for("login"))

@app.route('/logout/')
def logout():
    session['signed_user'] = None
    flash('Sessão encerrada com sucesso')
    return redirect(url_for("login"))
