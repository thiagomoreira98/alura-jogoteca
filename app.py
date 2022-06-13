from flask import Flask, render_template, request, redirect, session, flash, url_for
from models.game import Game
from models.user import User

app = Flask(__name__)
app.secret_key = 'alura'

list_games = [
    Game('God of War', 'Action', 'PS4'),
    Game('Forza Horizon', 'Corrida', 'Xbox')
]

users = {
    'admin': User('Admin', 'admin', 'admin123'),
    'common': User('Common', 'common', '123'),
}

@app.route("/")
def index():
    return render_template('list.html', title='Games', games=list_games)


@app.route("/new")
def new():
    if 'user' not in session or session['user'] is None:
        return redirect(url_for('login', next=url_for('new')))

    title = 'New Game'
    return render_template('form.html', title=title)


@app.route("/create", methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    platform = request.form['platform']
    game = Game(name, category, platform)
    list_games.append(game)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    user = request.form['user']
    password = request.form['password']
    next = request.form['next']

    if user in users:
        user_authenticate = users[user]
        if password == user_authenticate.password:
            session['user'] = user_authenticate.login
            flash(user_authenticate.login + ' logado com sucesso!')
            return redirect(next)

    flash('Usuario nao logado')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['user'] = None
    flash("Logout efetuado com sucesso!")
    return redirect(url_for('index'))


app.run()
