from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import Usuario, Curso

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"
app.config["SECRET_KEY"] = "123456"

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        senha_hash = generate_password_hash(request.form["senha"])
        # ativo = request.form.get("ativo", False) == "on"
        usuario = Usuario(name=name, email=email, senha=senha_hash)
        db.session.add(usuario)
        db.session.commit()
    usuarios = Usuario.query.all()
    return """
            <h1>Cadastro Realizado com Sucesso!</h1>
            <a href="/login">Fazer Login</a>
            """
            # render_template("cadastro.html", usuarios=usuarios)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["login-nome"]
        senha = request.form["login-senha"]
        email = request.form["login-email"]
        usuario = Usuario.query.filter_by(name=name, email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session["usuario_id"] = usuario.id
            return redirect(url_for("logado"))
        else:
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logado")
def logado():
    if "usuario_id" in session:
        usuario_id = session["usuario_id"]
        usuario = Usuario.query.get(usuario_id)
        return render_template("logado.html", usuario=usuario)
    else:
        return redirect(url_for("login"))


# cria as tabelas que ainda não existem, sem recriar as ja presentes
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
