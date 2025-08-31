from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

# ---------- BANCO DE DADOS ----------
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Cria a tabela caso não exista
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
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

       
        return redirect(url_for("index"))  # redireciona para a index

    return render_template("add.html")
      


 
# UPDATE (Editar)
@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    conn = get_db_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        conn.execute("UPDATE usuarios SET nome=?, email=? WHERE id=?", (nome, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

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

if __name__ == "__main__":
    app.run(debug=True)
