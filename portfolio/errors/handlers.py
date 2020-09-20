from flask import Blueprint, render_template

# create Blueprint for error pages
errors = Blueprint('errors', __name__)

# redirect to customised 404 error page if error is 404
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404

# redirect to customised 403 error page if error is 403
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('error_pages/403.html'), 403

# redirect to customised 500 error page if error is 500
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('error_pages/500.html'), 500