from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import string
import random
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class UrlEntry(db.Model):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    original_url = Column(String(255), nullable=False)
    short_url = Column(String(20), nullable=False, unique=True)

    def __init__(self, original_url, short_url):
        self.original_url = original_url
        self.short_url = short_url

    def __repr__(self):
        return '<UrlEntry %r>' % self.short_url

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
        original_url = data["url"]
        short_url = generate_random_string()

        new_url_entry = UrlEntry(original_url=original_url, short_url=short_url)

        db.session.add(new_url_entry)
        db.session.commit()

        return jsonify({"short_url": short_url})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True, host='backend', port=8000)

