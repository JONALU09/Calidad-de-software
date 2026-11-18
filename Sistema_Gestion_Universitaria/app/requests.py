from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db
from app.security import login_required

requests_bp = Blueprint("requests", __name__, url_prefix="/requests")

@requests_bp.get("/")
@login_required
def list_requests():
    rows = get_db().execute("""
        SELECT requests.*, students.full_name, students.code
        FROM requests JOIN students ON students.id = requests.student_id
        ORDER BY requests.id DESC
    """).fetchall()
    students = get_db().execute("SELECT id, full_name FROM students ORDER BY full_name").fetchall()
    return render_template("requests.html", rows=rows, students=students)

@requests_bp.post("/new")
@login_required
def create_request():
    student_id = request.form.get("student_id", type=int)
    request_type = request.form.get("request_type", "").strip()
    details = request.form.get("details", "").strip()
    if not student_id or not request_type or not details:
        flash("Completa todos los datos del trámite.", "error")
        return redirect(url_for("requests.list_requests"))
    db = get_db()
    db.execute(
        "INSERT INTO requests(student_id, request_type, details) VALUES (?, ?, ?)",
        (student_id, request_type, details),
    )
    db.commit()
    flash("Trámite registrado.", "success")
    return redirect(url_for("requests.list_requests"))

@requests_bp.post("/<int:request_id>/status")
@login_required
def update_status(request_id):
    status = request.form.get("status", "")
    allowed_statuses = {"Recibida", "En revisión", "En proceso", "Resuelta"}
    if status not in allowed_statuses:
        flash("Estado no válido.", "error")
        return redirect(url_for("requests.list_requests"))
    db = get_db()
    cursor = db.execute("UPDATE requests SET status=? WHERE id=?", (status, request_id))
    db.commit()
    if cursor.rowcount == 0:
        flash("No se encontró el trámite solicitado.", "error")
    else:
        flash("Estado actualizado.", "success")
    return redirect(url_for("requests.list_requests"))
