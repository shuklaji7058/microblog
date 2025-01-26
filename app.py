import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient
from werkzeug.serving import run_simple

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Add error handling for MongoDB connection
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        # Test the connection
        client.server_info()
        app.db = client.microblog
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

    @app.route("/", methods=["GET", "POST"])
    def home():
        try:
            if request.method == "POST":
                entry_content = request.form.get("content")
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
                app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

            entries_with_date = [
                (
                    entry["content"],
                    entry["date"],
                    datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
                )
                for entry in app.db.entries.find({})
            ]
            return render_template("home.html", entries=entries_with_date)
        except Exception as e:
            print(f"Error in home route: {e}")
            return "Database error occurred", 500

    return app