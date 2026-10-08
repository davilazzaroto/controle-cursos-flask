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

#Responsável por cadastrar o usuário e redirecionar para a página de cadastro
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
    return render_template("cadastro.html", usuarios=usuarios)


#REsponsável por tratar o erro 404 e redirecionar para a página de erro
@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

#Responsavel por fazer o login do usuário e redirecionar para a página de logado
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form["login-senha"]
        email = request.form["login-email"]
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session["usuario_id"] = usuario.id
            return redirect(url_for("cursos"))
        else:
            return redirect(url_for("login"))

    return render_template("login.html")

#Responsável por verificar se o usuário está logado e redirecionar para a página de logado
@app.route("/cursos", methods=['POST','GET'])
def cursos():
    if "usuario_id" in session:
        usuario_id = session["usuario_id"]
        usuario = db.session.get(Usuario, usuario_id)
        return render_template("cursos.html", usuario=usuario)
    else:
        return redirect(url_for("login"))

#Responsável por cadastrar o curso e redirecionar para a página de cadastro
@app.route("/novo-curso", methods=["GET", "POST"])
def novo_curso():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        usuario_id = session["usuario_id"]
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        plataforma = request.form["plataforma"]
        progresso = int(request.form.get("progresso", 0))
        status = int(request.form.get("status", 1))

        curso = Curso(
            usuario_id=usuario_id,
            titulo=titulo,
            descricao=descricao,
            plataforma=plataforma,
            progresso=progresso,
            status=status
        )
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for("cursos"))

    return render_template("novo_curso.html")

# O Flask pega o número passado na URL e injeta no parâmetro 'id' da função
@app.route("/cursos/<int:id>")
def detalhe_curso(id):

    if not "usuario_id" in session:
        return redirect(url_for("login"))

    curso = db.get_or_404(Curso, id)
    if curso.usuario_id == session["usuario_id"]:
        return render_template("detalhes_curso.html", curso=curso)
    else:
        return redirect(url_for("cursos"))

@app.route("/cursos/<int:id>/progresso", methods=["POST"])
def atualizar_progresso(id):
    if not "usuario_id" in session:
        return redirect(url_for("login"))

    curso = db.get_or_404(Curso, id)
    if curso and curso.usuario_id == session["usuario_id"]:
        curso.progresso = min((curso.progresso or 0) + 10, 100)
        if curso.progresso == 100:
            curso.status = 2  # Marca como concluído
        db.session.commit()
        return redirect(url_for("detalhe_curso", id=curso.id))
    else:
        return redirect(url_for("cursos"))

@app.route("/cursos/<int:id>/excluir", methods=["POST",'GET'])
def excluir_curso(id):
    if not "usuario_id" in session:
        return redirect(url_for("login"))

    curso = Curso.query.get(id)
    if curso and curso.usuario_id == session["usuario_id"]:
        db.session.delete(curso)
        db.session.commit()
    return redirect(url_for("cursos"))

# cria as tabelas que ainda não existem, sem recriar as ja presentes
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
