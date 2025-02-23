# **Image Processing API 🚀**

## **Overview**  
This is a Flask-based **asynchronous image processing API** that:  
✅ Accepts a **CSV file** with image URLs.  
✅ Processes images asynchronously using **Celery**.  
✅ Stores processed images in **Cloudinary**.  
✅ Maintains processing status in **MongoDB**.  
✅ Provides APIs to check processing status.  

---

## **🛠️ Tech Stack**
- **Backend:** Flask, Celery  
- **Database:** MongoDB  
- **Message Broker:** Redis  
- **Storage:** Cloudinary  
- **Task Queue:** Celery  

---

## **⚙️ Features**
✔ **Upload images** via CSV.  
✔ **Asynchronous processing** for better scalability.  
✔ **Webhook integration** for status updates.  
✔ **Cloudinary storage** for processed images.  
✔ **MongoDB persistence** for tracking requests.  

---
## **🛠️ Setup Instructions**
# 1️⃣ Clone the Repository
git clone https://github.com/RANJEETIITJ/image-processing.git
cd image-processing

# 2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate  # For Windows

# 3️⃣ Install Dependencies
pip install -r requirements.txt

# 4️⃣ Set Up Environment Variables
# Create a .env file and add:
CLOUDINARY_CLOUD_NAME="YOUR_CLOUD_NAME"
CLOUDINARY_API_KEY="YOUR KEY"
CLOUDINARY_API_SECRET="SECRET_KEY"
MONGO_URI="your_mongodb_connection_string"
broker_url = "REDIS_BROKER_URL"
result_backend = "REDIS_URL"
WEBHOOK_URL = "WEBHOOK_ENDPOINT" 

# 5️⃣ Start Flask Server
python run.py

# 6️⃣ Start Celery Worker
celery -A celery_tasks.tasks worker --loglevel=info --pool=solo

