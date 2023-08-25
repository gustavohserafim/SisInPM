from werkzeug.middleware.proxy_fix import ProxyFix
from sisinpm_app import create_app
import logging

gunicorn_logger = logging.getLogger('gunicorn.error')

application = create_app(logger_override=gunicorn_logger)
application.wsgi_app = ProxyFix(application.wsgi_app, x_for=1, x_host=1)