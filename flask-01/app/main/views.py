from datetime import datetime
from flask import current_app, render_template, session, redirect, url_for, flash

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email


@main.route("/user/<name>")
def user(name):
    # return '<h1>Hello, %s!<h1' % name
    return render_template('user.html', name=name)


@main.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        app = current_app._get_current_object()
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'Nemail', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())
