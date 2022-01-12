from flask import flash, Flask, render_template, redirect, request, session, url_for

host, port = "0.0.0.0", 5000
app = Flask(__name__)
app.secret_key = 'secret_key'

class Game:
    def __init__(self, name, category, console) -> None:
        self.name = name
        self.category = category
        self.console = console

tetris = Game("Tetris", "Puzzle", "PC")
super_mario = Game("Super Mario", "Plataforma", "SNES")
pokemon_gold = Game("Pokemon Gold", "RPG", "GBA")
mortal_kombat = Game("Mortal Kombat", "Luta", "SNES")
games = [tetris, super_mario, pokemon_gold, mortal_kombat,]

class User:
    def __init__(self, pk, username, password) -> None:
        self.pk = pk
        self.username = username
        self.password = password

administrator = User(0, "admin", "password")
mateus = User(1, "Mateus", "123456")
users = { administrator.username : administrator, mateus.username : mateus, }

def has_signed_user() -> bool:
    return "signed_user" in session and session["signed_user"] != None

@app.route("/")
@app.route("/games")
def index():
    if not has_signed_user():
        return redirect(url_for("login", next=url_for("index")))
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
    games.append(game)
    return redirect(url_for("index"))

@app.route("/login/")
def login():
    next = request.args.get("next")
    return render_template("login.html", next=next)

@app.route("/authenticate/", methods=["POST",])
def authenticate():
    username = request.form["username"]
    password = request.form["password"]
    next = request.form["next"]
    user = users[username]
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

app.run(debug=True, host=host, port=port)