from flask import Blueprint, request, jsonify
import uuid
import pandas as pd
from app.models import insert_request, update_request
from celery_tasks.tasks import process_images
from app import mongo
bp = Blueprint("main", __name__)

@bp.route("/upload", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    df = pd.read_csv(file)

    if not all(col in df.columns for col in ["S. No.", "Product Name", "Input Image Urls"]):
        return jsonify({"error": "Invalid CSV format"}), 400
    request_id = str(uuid.uuid4())
    for ind, row in df.iterrows():
        product_name = row["Product Name"]
        input_urls = row["Input Image Urls"].split(",")

        insert_request(request_id, product_name, input_urls)

        process_images.delay(request_id, product_name, input_urls,ind)

    return jsonify({"request_id": request_id}), 200



@bp.route("/status/<request_id>", methods=["GET"])
def check_status(request_id):
    request_data = mongo.db.processed_images.find_one({"request_id": request_id})
    webhook_data = mongo.db.webhook_logs.find_one({"request_id": request_id}, {"_id": 0})

    if not request_data:
        return jsonify({"error": "Request ID not found"}), 404

    return jsonify({
        "request_id": request_data["request_id"],
        "status": request_data["status"],
        "output_csv": webhook_data['output_csv'] 
    })


@bp.route("/webhook", methods=["POST"])
def webhook_listener():
    """Receives webhook events and logs them."""
    data = request.json 

    mongo.db.webhook_logs.insert_one(data)

    return jsonify({"message": "Webhook received"}), 200
