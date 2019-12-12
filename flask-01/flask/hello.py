import sys
import os

from flask import Flask, render_template, session, redirect, url_for, flash
from flask import request
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy

from flask_mail import Message
from flask_mail import Mail

# 异步发送邮件
from threading import Thread


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# 跨站请求伪造保护SCRF
app.config['SECRET_KEY'] = 'hard to guess string'


app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
# app.config['MAIL_USE_SSL'] = True

app.config['MAIL_USERNAME'] = 'lustyle2010@163.com'
app.config['FLASKY_ADMIN'] = 'it-zyk@outlook'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Lustyle]'
app.config['FLASKY_MAIL_SENDER'] = 'lustyle2010@163.com'

# db对象是SQLAlchemy类的实例，表示程序使用的数据库，同时还获得了Flask-SQLAlchemy提供的所有功能。
db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)

bootstrap = Bootstrap(app)


moment = Moment(app)

mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

# def send_email(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     mail.send(msg)


@app.route("/user/<name>")
def user(name):
    # return '<h1>Hello, %s!<h1' % name
    return render_template('user.html', name=name)


@app.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    # return '<p> Your browser is %s</p>' % user_agent
    # return render_template('index.html',
    #                        current_time=datetime.utcnow())
    name = None
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['MAIL_USERNAME'], 'New User',
                           'Nemail', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())

    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     form.name.data = ''
    #     return redirect(url_for('index'))
    # return render_template('index.html',
    #                        form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())

    # name = None
    # form = NameForm()
    # if form.validate_on_submit():
    #     old_name = session.get('name')
    #     if old_name is not None and old_name != form.name.data:
    #         flash('Looks like you have changed your name!')
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))
    # return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


if __name__ == '__main__':
    manager.add_command("shell", Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)
    manager.run()
    # app.run(debug=True)
