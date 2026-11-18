from app.db import get_db

def test_login_page_is_available(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Bienvenido" in response.data

def test_login_rejects_invalid_password(client):
    response = client.post("/auth/login", data={"username": "admin", "password": "incorrecta"})
    assert response.status_code == 200
    assert b"incorrectos" in response.data

def test_students_route_requires_login(client):
    response = client.get("/students/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]

def test_create_student(logged_client):
    response = logged_client.post("/students/new", data={
        "code": "A001", "full_name": "Ana López",
        "email": "ana@example.com", "career": "Ingeniería de Software"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Ana L\xc3\xb3pez" in response.data

def test_duplicate_student_code_is_handled(logged_client):
    data = {"code": "A001", "full_name": "Ana López", "email": "ana@example.com", "career": "Software"}
    logged_client.post("/students/new", data=data)
    response = logged_client.post("/students/new", data={**data, "full_name": "Ana Pérez"})
    assert response.status_code == 200
    assert b"No se pudo registrar" in response.data

def test_grade_range_validation(logged_client, app):
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO students(code,full_name,email,career) VALUES('A002','Luis','luis@example.com','TI')")
        student_id = db.execute("SELECT id FROM students WHERE code='A002'").fetchone()["id"]
        subject_id = db.execute("SELECT id FROM subjects LIMIT 1").fetchone()["id"]
        db.commit()
    response = logged_client.post("/academic/grades", data={
        "student_id": student_id, "subject_id": subject_id, "grade": 120
    }, follow_redirects=True)
    assert b"calificaci\xc3\xb3n de 0 a 100" in response.data

def test_request_creation_and_status_update(logged_client, app):
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO students(code,full_name,email,career) VALUES('A003','Eva','eva@example.com','TI')")
        student_id = db.execute("SELECT id FROM students WHERE code='A003'").fetchone()["id"]
        db.commit()
    response = logged_client.post("/requests/new", data={
        "student_id": student_id, "request_type": "Constancia de estudios", "details": "Para beca"
    }, follow_redirects=True)
    assert b"Constancia de estudios" in response.data
    response = logged_client.post("/requests/1/status", data={"status": "Resuelta"}, follow_redirects=True)
    assert b"Resuelta" in response.data


def test_student_rejects_invalid_email(logged_client):
    response = logged_client.post("/students/new", data={
        "code": "A004", "full_name": "Mario", "email": "correo-invalido",
        "career": "Informática"
    })
    assert b"correo electr" in response.data

def test_missing_request_id_is_reported(logged_client):
    response = logged_client.post("/requests/999/status", data={"status": "Resuelta"}, follow_redirects=True)
    assert b"No se encontr" in response.data


def test_invalid_request_status_is_rejected(logged_client):
    response = logged_client.post("/requests/1/status", data={"status": "Inventado"}, follow_redirects=True)
    assert b"Estado no v" in response.data
