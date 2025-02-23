from app import mongo, create_app 
from app.models import update_request
import requests
from dotenv import load_dotenv
from PIL import Image
from app.celery import celery
import cloudinary
import cloudinary.uploader
import os
import csv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@celery.task
def process_images(request_id, product_name, input_urls, ind):
    processed_images = []

    app = create_app()
    with app.app_context():
        for index, url in enumerate(input_urls):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                img = Image.open(response.raw)
                img = img.convert("RGB")

                filename = f"{request_id}_{index}_{ind}.jpg"
                temp_path = os.path.join("/tmp", filename)
                img.save(temp_path, "JPEG", quality=50)

                upload_result = cloudinary.uploader.upload(temp_path)
                processed_image_url = upload_result["secure_url"]

                processed_images.append(processed_image_url)

                os.remove(temp_path)

        update_request(request_id, product_name, input_urls, processed_images)

        cloudinary_csv_url = generate_output_csv(request_id)

        webhook_response = trigger_webhook(request_id, processed_images, cloudinary_csv_url)
        return webhook_response

def trigger_webhook(request_id, output_urls, output_csv_url):
    """Send a webhook notification when processing completes."""
    # webhook_url = "http://127.0.0.1:5000/webhook" 
    webhook_url = os.getenv("WEBHOOK_URL")
    payload = {
        "request_id": request_id,
        "output_urls": output_urls,
        "output_csv": output_csv_url  
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status() 
        return response.text 
    except requests.exceptions.RequestException as e:
        return f"Webhook failed: {str(e)}"



def generate_output_csv(request_id):
    """Generate an output CSV file and upload it to Cloudinary."""
    data = list(mongo.db.processed_images.find({"request_id": request_id}))

    if not data:
        return None

    temp_folder = "/tmp" 
    os.makedirs(temp_folder, exist_ok=True)

    output_filename = os.path.join(temp_folder, f"{request_id}_output.csv")

    with open(output_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Serial Number", "Product Name", "Input Image Urls", "Output Image Urls"]) 

        for index, record in enumerate(data, start=1):
            writer.writerow([
                index,
                record["product_name"],
                ",".join(record["input_urls"]),
                ",".join(record["processed_images"])
            ])

    #  Upload CSV to Cloudinary
    upload_result = cloudinary.uploader.upload(output_filename, resource_type="raw")
    cloudinary_csv_url = upload_result["secure_url"]

    os.remove(output_filename)

    # print(f" CSV uploaded to Cloudinary: {cloudinary_csv_url}")
    return cloudinary_csv_url
