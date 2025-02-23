from celery import Celery
from config import Config

celery = Celery(
    "image_processor",
    broker=Config.broker_url,
    backend=Config.result_backend
)

def init_celery(app):
    """Attach Flask app config to Celery."""
    celery.conf.update(app.config)
    celery.conf.broker_transport_options = {
        "ssl": {"ssl_cert_reqs": "CERT_REQUIRED"} 
    }
    celery.conf.result_backend_transport_options = {
        "ssl_cert_reqs": "CERT_REQUIRED"}
