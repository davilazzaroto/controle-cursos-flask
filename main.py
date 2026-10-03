from flask import Flask,render_template, request,url_for, redirect
from db import db
from models import Usuario,Curso


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///dados.db'
app.config["SECRET_KEY"] = "123456" 

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/usuarios', methods=['GET','POST'])
def usuarios():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        ativo = request.form.get('ativo', False) == 'on'
        usuario = Usuario(name=name, email=email, ativo=ativo)
        db.session.add(usuario)
        db.session.commit()
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)


# cria as tabelas que ainda não existem, sem recriar as ja presentes
if __name__  == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
        
