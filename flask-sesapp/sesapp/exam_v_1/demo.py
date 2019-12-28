
from . import exam
import logging
from flask import g, current_app, render_template
from sesapp.utils.commons import login_required


@exam.route("/index")
@login_required
def index():
    # current_app.logger.error("error msg")
    # current_app.logger.warn("warn msg")
    # current_app.logger.warn("warn msg")
    # current_app.logger.infso("info msg")
    # current_app.logger.debug("debug msg")
    return render_template(
        'layout.html',
        name=g.username
    )
    return "index page"
