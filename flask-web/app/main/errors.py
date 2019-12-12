from flask import render_template
from . import main


"""在蓝本中编写错误处理程序有点不同，如果使用errorhandler修饰器，那么只有蓝本中的错误才会触发。如果想注册全局的错误处理程序，要用app_errorhandler"""


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
