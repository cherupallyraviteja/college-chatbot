from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from main import handle_user_query

app = Flask(__name__)

TWILIO_ACCOUNT_SID="AYajjmpDLunawN9mRtBUbWAMSNG9on1NRL"
TWILIO_AUTH_TOKEN=""
TWILIO_WHATSAPP_NUMBER="+18453662660"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body")
    from_number = request.form.get("From")

    bot_reply = handle_user_query(incoming_msg)

    resp = MessagingResponse()
    resp.message(bot_reply)

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
