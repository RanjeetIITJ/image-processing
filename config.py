import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    # MONGO_URI = "mongodb://localhost:27017/image_processor"
    MONGO_URI = os.getenv("MONGO_URI")
    broker_url = os.getenv("broker_url")
    result_backend = os.getenv("result_backend")
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "ssl": {"ssl_cert_reqs": "CERT_NONE"}
    }
    CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
        "ssl_cert_reqs": "CERT_NONE"
    }
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
