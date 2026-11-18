# Sistema de Gestión Universitaria (SGU)

Aplicación web académica desarrollada con Python, Flask y SQLite.

## Funcionalidades
- Inicio y cierre de sesión con contraseña almacenada mediante hash.
- Registro y consulta de estudiantes.
- Registro y consulta de calificaciones (0 a 100).
- Registro de trámites y actualización de sus estados.
- Base de datos relacional SQLite.

## Requisitos
- Python 3.10 o superior.

## Instalación y ejecución (Windows)
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py run.py
```
Abrir http://127.0.0.1:5000

## Usuario de demostración
- Usuario: `admin`
- Contraseña: `Admin123!`

Cambiar `SECRET_KEY` mediante variable de entorno antes de cualquier despliegue real. La cuenta de demostración es únicamente para uso académico local.

## Pruebas
```powershell
pytest -v
```

## Estructura
- `app/`: aplicación Flask y módulos funcionales.
- `app/templates/`: vistas HTML con Jinja.
- `app/static/`: estilos CSS.
- `tests/`: pruebas automatizadas.
- `run.py`: punto de entrada.
