from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db
from app.security import login_required

academic_bp = Blueprint("academic", __name__, url_prefix="/academic")

@academic_bp.get("/")
@login_required
def grades():
    db = get_db()
    rows = db.execute("""
        SELECT students.full_name, students.code, subjects.name AS subject, grades.grade
        FROM grades
        JOIN students ON students.id = grades.student_id
        JOIN subjects ON subjects.id = grades.subject_id
        ORDER BY students.full_name, subjects.name
    """).fetchall()
    students = db.execute("SELECT id, full_name FROM students ORDER BY full_name").fetchall()
    subjects = db.execute("SELECT id, name FROM subjects ORDER BY name").fetchall()
    return render_template("grades.html", rows=rows, students=students, subjects=subjects)

@academic_bp.post("/grades")
@login_required
def save_grade():
    student_id = request.form.get("student_id", type=int)
    subject_id = request.form.get("subject_id", type=int)
    grade = request.form.get("grade", type=float)
    if not student_id or not subject_id or grade is None or not 0 <= grade <= 100:
        flash("Selecciona estudiante y materia e ingresa una calificación de 0 a 100.", "error")
        return redirect(url_for("academic.grades"))
    db = get_db()
    try:
        db.execute("""
            INSERT INTO grades(student_id, subject_id, grade) VALUES (?, ?, ?)
            ON CONFLICT(student_id, subject_id) DO UPDATE SET grade=excluded.grade
        """, (student_id, subject_id, grade))
        db.commit()
        flash("Calificación guardada.", "success")
    except Exception:
        db.rollback()
        flash("No se pudo guardar la calificación.", "error")
    return redirect(url_for("academic.grades"))
