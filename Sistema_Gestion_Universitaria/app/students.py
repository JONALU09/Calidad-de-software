import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db
from app.security import login_required
import re

students_bp = Blueprint("students", __name__, url_prefix="/students")

@students_bp.get("/")
@login_required
def list_students():
    students = get_db().execute(
        "SELECT * FROM students ORDER BY full_name"
    ).fetchall()
    return render_template("students.html", students=students)

@students_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_student():
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        career = request.form.get("career", "").strip()
        if not all([code, full_name, email, career]):
            flash("Todos los campos son obligatorios.", "error")
            return render_template("student_form.html")
        if len(code) > 20 or len(full_name) > 100 or len(career) > 100:
            flash("Uno o más campos exceden la longitud permitida.", "error")
            return render_template("student_form.html")
        if not re.fullmatch(r"[^@\\s]+@[^@\\s]+\\.[^@\\s]+", email):
            flash("Ingresa un correo electrónico válido.", "error")
            return render_template("student_form.html")
        try:
            get_db().execute(
                "INSERT INTO students(code, full_name, email, career) VALUES (?, ?, ?, ?)",
                (code, full_name, email, career),
            )
            get_db().commit()
            flash("Estudiante registrado.", "success")
            return redirect(url_for("students.list_students"))
        except sqlite3.IntegrityError:
            get_db().rollback()
            flash("La matrícula ya está registrada.", "error")
    return render_template("student_form.html")
