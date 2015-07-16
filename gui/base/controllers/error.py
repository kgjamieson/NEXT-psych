from flask import Blueprint, render_template

from base import cache
import traceback
error = Blueprint('error', __name__)

@error.app_errorhandler(400)
def _400(error):
	trace = traceback.format_exc()
	return render_template('error.html', error=error, trace=trace), 400

@error.app_errorhandler(403)
def _403(error):
	trace = traceback.format_exc()
	return render_template('error.html', error=error, trace=trace), 403

@error.app_errorhandler(404)
def _404(error):
	trace = traceback.format_exc()
	return render_template('error.html', error=error, trace=trace), 404

@error.app_errorhandler(410)
def _410(error):
	trace = traceback.format_exc()
	return render_template('error.html', error=error, trace=trace), 410

@error.app_errorhandler(500)
def _500(error):
	trace = traceback.format_exc()
	return render_template('error.html', error=error, trace=trace), 500