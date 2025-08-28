import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash
from personal_website.db import get_connection
 
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
 
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM users WHERE email = %s', (email,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        error = None
        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'
 
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('admin.admin'))
        flash(error)
    return render_template('auth/login.html')
 
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))