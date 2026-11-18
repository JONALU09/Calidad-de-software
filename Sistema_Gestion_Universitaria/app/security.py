from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("user_id"):
            flash("Inicia sesión para continuar.", "error")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view
