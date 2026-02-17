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
    """Handle Package Inquiry Form (Multi-step form from Contact Page)"""
    try:
        data = request.get_json()

        # Validate required fields
        required = ["fullName", "email", "phone", "departureCity", "travelMonth", "departureDate", "packageTier", "roomType"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"success": False, "error": f"Missing fields: {', '.join(missing)}"}), 400

        # Check for Ramadan discount
        departure_date = data.get("departureDate", "")
        is_ramadan_discount = False
        if departure_date:
            from datetime import datetime
            try:
                date_obj = datetime.strptime(departure_date, "%Y-%m-%d")
                ramadan_start = datetime(2026, 2, 18)
                ramadan_end = datetime(2026, 3, 18)
                is_ramadan_discount = ramadan_start <= date_obj <= ramadan_end
            except ValueError:
                pass
        
        data["ramadanDiscount"] = is_ramadan_discount

        send_inquiry_email(data)

        return jsonify({
            "success": True, 
            "message": "Inquiry submitted successfully. We'll get back to you within 24 hours!",
            "ramadanDiscount": is_ramadan_discount
        }), 200

    except Exception as e:
        print(f"[ERROR] Inquiry submission failed: {e}")
        return jsonify({"success": False, "error": "Something went wrong. Please try again later."}), 500


@app.route("/api/contact", methods=["POST"])
def handle_contact():
    """Handle Contact Page general messages"""
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
    return jsonify({"status": "ok", "message": "Haram Umrah Travels API is running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=Config.DEBUG)