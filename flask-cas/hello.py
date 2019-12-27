from flask import Flask
from flask_cas import CAS
from flask_cas import login_required

app = Flask(__name__)
cas = CAS(app, '/cas')
app.config['CAS_SERVER'] = 'https://cas.china-tcc.com'
app.config['CAS_AFTER_LOGIN'] = 'route_root'

@app.route('/')
@login_required
def route_root():
    return flask.render_template(
        'layout.html',
        username = cas.username,
        display_name = cas.attributes['cas:displayName']
    )

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
