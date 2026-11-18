import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")
    DATABASE = os.environ.get("DATABASE_PATH", "instance/universidad.db")
