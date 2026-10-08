# Controle de Cursos

Aplicação em desenvolvimento para organizar cursos e acompanhar o progresso dos estudos.

## Tecnologias

Python, Flask, Flask-SQLAlchemy, SQLite, HTML e CSS.

## Funcionalidades

- Cadastro e login de usuários.
- Cadastro, listagem, detalhes e exclusão dos próprios cursos.
- Aumento do progresso em 10 pontos percentuais por clique, até 100%, marcando o curso como concluído.

## Como executar

No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install Flask Flask-SQLAlchemy
.\.venv\Scripts\python.exe main.py
```

Acesse http://127.0.0.1:5000. O banco `instance/dados.db` é criado automaticamente na primeira execução.

O projeto usa modo debug e uma chave de sessão fixa para desenvolvimento local; ainda não está preparado para produção.
