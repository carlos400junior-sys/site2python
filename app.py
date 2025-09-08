from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = "usuarios.db"


# ---------- CONEXÃO COM O BANCO DE DADOS ----------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Retorna dicionário em vez de tupla
    return conn


# ---------- CRIAR TABELA (executar uma vez) ----------
def init_db():
    if not os.path.exists(DATABASE):
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')
            conn.commit()

# ---------- ROTAS CRUD ----------

# READ (Listar todos)
@app.route("/")
def index():
    conn = get_db_connection()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()
    return render_template("index.html", usuarios=usuarios)


# CREATE (Adicionar)
@app.route("/add", methods=("GET", "POST"))
def add():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        conn = get_db_connection()
        conn.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")


# UPDATE (Editar)
@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    conn = get_db_connection()

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        conn.execute("UPDATE usuarios SET nome=?, email=? WHERE id=?", (nome, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", usuario=usuario)


# DELETE (Excluir)
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


# ---------- INICIAR APP ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
