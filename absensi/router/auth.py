from app import api, app
from flask import Blueprint, redirect, url_for
from flask_login import logout_user, login_required
from absensi.resource.login import LoginResource


auth = Blueprint('auth', __name__)


api.add_resource(LoginResource, '/login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('loginresource'))
# @app.route('/login')
# def login():
#     return render_template('login.html')
