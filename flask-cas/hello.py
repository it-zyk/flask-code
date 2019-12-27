from flask import Flask
from flask_cas import CAS
from flask_cas import login_required
from flask_cas import login
from flask_cas import logout

app = Flask(__name__)
cas = CAS(app, '/cas')
app.config['CAS_SERVER'] = 'https://cas.china-tcc.com'
app.config['CAS_AFTER_LOGIN'] = 'route_root'

app.config['SECRET_KEY'] = "KAEJF34KAK12344DFJAI"

@app.route('/')
@login_required
def route_root():
    return flask.render_template(
        'layout.html',
        username=cas.username
    )

#
# @app.route('/')
# def index():
#     return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
