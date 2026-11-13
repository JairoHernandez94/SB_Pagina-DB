import os
import re
import secrets
from functools import wraps

import mysql.connector
from dotenv import load_dotenv
from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for, abort)
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

PRODUCTOS = [
    {"nombre": "Lavanda & Manzana", "desc": "Infusión floral con manzana deshidratada.", "icono": "🍎"},
    {"nombre": "Manzanilla Dorada", "desc": "Flores enteras con un toque de canela.", "icono": "🌼"},
    {"nombre": "Fresa & Clavo", "desc": "Frutos rojos con especias cálidas.", "icono": "🍓"},
    {"nombre": "Canela & Anís", "desc": "Mezcla especiada para tardes frías.", "icono": "🌟"},
]


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "sabores_babilonia"),
    )


def login_required(view):
    @wraps(view)
    def wrapped(*a, **kw):
        if "user_id" not in session:
            flash("Inicia sesión para continuar.", "info")
            return redirect(url_for("login"))
        return view(*a, **kw)
    return wrapped


@app.before_request
def csrf_protect():
    if request.method == "POST":
        if not secrets.compare_digest(
            request.form.get("csrf_token", ""), session.get("csrf_token", "")
        ):
            abort(400, "Token CSRF inválido")


@app.context_processor
def inject_globals():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return {"csrf_token": session["csrf_token"], "empresa": "Sabores de Babilonia",
            "slogan": "Tés y frutos premium"}


@app.route("/")
def index():
    return render_template("index.html", productos=PRODUCTOS)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefono = request.form.get("telefono", "").strip() or None
        password = request.form.get("password", "")
        confirmar = request.form.get("confirmar", "")

        errores = []
        if len(nombre) < 2:
            errores.append("Escribe tu nombre.")
        if not EMAIL_RE.match(email):
            errores.append("Correo no válido.")
        if len(password) < 8:
            errores.append("La contraseña debe tener al menos 8 caracteres.")
        if password != confirmar:
            errores.append("Las contraseñas no coinciden.")

        if not errores:
            try:
                db = get_db()
                cur = db.cursor()
                cur.execute("SELECT id FROM usuarios WHERE email=%s", (email,))
                if cur.fetchone():
                    errores.append("Ese correo ya está registrado.")
                else:
                    cur.execute(
                        "INSERT INTO usuarios (nombre, email, telefono, password_hash)"
                        " VALUES (%s,%s,%s,%s)",
                        (nombre, email, telefono, generate_password_hash(password)),
                    )
                    db.commit()
                    flash("¡Registro exitoso! Ya puedes ingresar.", "ok")
                    return redirect(url_for("login"))
            except mysql.connector.Error:
                app.logger.exception("Error de base de datos en registro")
                errores.append("No pudimos conectar con la base de datos.")
            finally:
                try:
                    cur.close(); db.close()
                except Exception:
                    pass
        for e in errores:
            flash(e, "error")
    return render_template("registro.html")


@app.route("/ingreso", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        try:
            db = get_db()
            cur = db.cursor(dictionary=True)
            cur.execute("SELECT id, nombre, password_hash, rol FROM usuarios WHERE email=%s", (email,))
            user = cur.fetchone()
            if user and check_password_hash(user["password_hash"], password):
                cur.execute("UPDATE usuarios SET ultimo_ingreso=NOW() WHERE id=%s", (user["id"],))
                db.commit()
                session.clear()
                session.update(user_id=user["id"], nombre=user["nombre"], rol=user["rol"])
                return redirect(url_for("panel"))
            flash("Correo o contraseña incorrectos.", "error")
        except mysql.connector.Error:
            app.logger.exception("Error de base de datos en ingreso")
            flash("No pudimos conectar con la base de datos.", "error")
        finally:
            try:
                cur.close(); db.close()
            except Exception:
                pass
    return render_template("login.html")


@app.route("/panel")
@login_required
def panel():
    return render_template("panel.html")


@app.route("/salir", methods=["POST"])
def salir():
    session.clear()
    flash("Sesión cerrada. ¡Vuelve pronto!", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)