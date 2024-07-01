import string
import random
import os
from flask import Flask, redirect, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

CORS(app)

def get_db():
    mongo_uri = os.environ.get('MONGO_URI')
    client = MongoClient(mongo_uri)

    db = client["urldb"]

    return db

db = get_db()

def generate_random_string():
    length = 6
    letters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

@app.route('/', methods=['POST'])
def short_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing requests data"}), 400
    
    try:

       collection = db["url"]
       short = generate_random_string()
       url = {
            "original_url": data["url"],
            "short_url": short,
        }

       collection_id = collection.insert_one(url).inserted_id

       return jsonify({"data": {"id": str(collection_id), "url": short }})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/<short_url>')
def redirect_to_url(short_url):
    collection = db["url"]
    url_mapping = collection.find_one({'short_url': short_url})

    if url_mapping:
        return redirect(url_mapping['original_url'])
    else:
        return jsonify({"message: Short URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

