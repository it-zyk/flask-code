
from . import sesexam
import logging
from flask import current_app, g
from sesapp.utils.commons import login_required


@login_required
@exam.route("/index")
def index():
    # current_app.logger.error("error msg")
    # current_app.logger.warn("warn msg")
    # current_app.logger.warn("warn msg")
    # current_app.logger.info("info msg")
    # current_app.logger.debug("debug msg")
    return render_template(
        'layout.html',
        name=g.username
    )
    return "index page"