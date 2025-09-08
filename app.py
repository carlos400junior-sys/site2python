from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ---------- CONEXÃO COM O BANCO DE DADOS (MySQL) ----------
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",       # host correto
        port=3306,              # porta padrão do MySQL no XAMPP
        user="root",            # padrão do XAMPP
        password="",            # padrão do XAMPP (sem senha)
        database="meubanco2"    # seu banco de dados
    )
    return conn


# ---------- CRIAR TABELA (executar uma vez) ----------
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()


# ---------- ROTAS CRUD ----------

# READ (Listar todos)
@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", usuarios=usuarios)


# CREATE (Adicionar)
@app.route("/add", methods=("GET", "POST"))
def add():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")


# UPDATE (Editar)
@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        cursor.execute("UPDATE usuarios SET nome=%s, email=%s WHERE id=%s", (nome, email, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit.html", usuario=usuario)


# DELETE (Excluir)
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))


# ---------- INICIAR APP ----------
if __name__ == "__main__":
    app.run(debug=True)

