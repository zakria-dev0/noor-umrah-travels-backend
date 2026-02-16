# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.mailer import send_inquiry_email, send_contact_email
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=Config.ALLOWED_ORIGINS)


@app.route("/api/inquiry", methods=["POST"])
def handle_inquiry():
    """Handle Package Inquiry Form (Homepage + Contact Page)"""
    try:
        data = request.get_json()

        # Validate required fields
        required = ["fullName", "email", "phone", "packageType"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"success": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

        send_inquiry_email(data)

        return jsonify({"success": True, "message": "Inquiry submitted successfully. We'll get back to you shortly!"}), 200

    except Exception as e:
        print(f"[ERROR] Inquiry submission failed: {e}")
        return jsonify({"success": False, "error": "Something went wrong. Please try again later."}), 500


@app.route("/api/contact", methods=["POST"])
def handle_contact():
    """Handle Contact Page general messages (if you add a simple message form later)"""
    try:
        data = request.get_json()

        required = ["fullName", "email", "message"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"success": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

        send_contact_email(data)

        return jsonify({"success": True, "message": "Message sent successfully!"}), 200

    except Exception as e:
        print(f"[ERROR] Contact submission failed: {e}")
        return jsonify({"success": False, "error": "Something went wrong. Please try again later."}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Noor Umrah Travels API is running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=Config.DEBUG)