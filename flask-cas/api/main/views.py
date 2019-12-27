from . import main
from flask import current_app, render_template, session, redirect, url_for, flash
from flask_cas import login_required

@main.route("/user")
@login_required
def user(name):
    # return '<h1>Hello, %s!<h1' % name
    name = cas.username
    return render_template('user.html', name=name)
