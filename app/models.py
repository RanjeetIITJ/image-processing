from app import mongo

def insert_request(request_id, product_name, input_urls):
    """Store the initial request details in MongoDB."""
    mongo.db.processed_images.insert_one({
        "request_id": request_id,
        "product_name": product_name,
        "input_urls": input_urls,
        "processed_images": [],
        "status": "pending"
    })


def update_request(request_id, product_name, input_urls, processed_images):
    """Update MongoDB with input and output image URLs."""
    mongo.db.processed_images.update_one(
        {"request_id": request_id, "product_name": product_name},
        {"$set": {
            "input_urls": input_urls,
            "processed_images": processed_images,
            "status": "completed"
        }}
    )