from flask import Flask,render_template, request
from db import db
from models import Usuario,Curso


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///dados.db'
app.config["SECRET_KEY"] = "123456" 

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

# cria as tabelas que ainda não existem, sem recriar as ja presentes
if __name__  == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
        
