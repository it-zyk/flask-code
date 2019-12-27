from flask import Flask, render_template
from flask_cas import CAS
from flask_cas import login_required
from flask_cas import login
from flask_cas import logout

app = Flask(__name__)

app.config['CAS_SERVER'] = 'https://cas.china-tcc.com'
app.config['CAS_AFTER_LOGIN'] = 'root'

app.config['SECRET_KEY'] = "KAEJF34KAK12344DFJAI"
cas = CAS(app, '/cas')

@app.route('/')
@login_required
def route_root():
    return render_template(
        'layout.html',
        username=cas.username
    )

#
# @app.route('/')
# def index():
#     return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
