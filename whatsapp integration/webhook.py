from flask import Flask, request
import os
from main import handle_whatsapp_message
from meta_whatsapp import send_whatsapp_message

app = Flask(__name__)

# Step 1: Verification (required by Meta)
@app.route("/webhook", methods=["GET"])
def verify():
    if (
        request.args.get("hub.mode") == "subscribe"
        and request.args.get("hub.verify_token") == os.getenv("META_VERIFY_TOKEN")
    ):
        return request.args.get("hub.challenge"), 200
    return "Verification failed", 403


# Step 2: Receive messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        message = value["messages"][0]

        user_text = message["text"]["body"]
        from_number = message["from"]

        # Call your chatbot pipeline
        reply = handle_whatsapp_message(user_text, from_number)

        # Send response
        send_whatsapp_message(from_number, reply)

    except Exception:
        pass

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    app.run(port=5000)
