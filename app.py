import requests
import os
from flask import Flask, request, jsonify
from agent import get_reply
from dotenv import load_dotenv
from flask import send_from_directory

load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

print("VERIFY_TOKEN:", VERIFY_TOKEN)
print("PAGE_ACCESS_TOKEN:", PAGE_ACCESS_TOKEN)

app = Flask(__name__)


@app.route("/reply", methods=["POST"])
def reply():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "message required"}), 400

    response = get_reply(message)

    return jsonify({
        "user_message": message,
        "reply": response
    })
    
    
def send_message(recipient_id, text):

    url = f"https://graph.facebook.com/v25.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    response = requests.post(url, json=payload)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)
   
    
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Verification failed"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print("FULL DATA:", data)

    if "entry" in data:
        for entry in data["entry"]:
            for msg in entry["messaging"]:

                print("MESSAGE OBJECT:", msg)

                sender_id = msg["sender"]["id"]

                if msg.get("message") and not msg["message"].get("is_echo"):

                    user_msg = msg["message"].get("text")

                    print("USER MESSAGE:", user_msg)

                    if user_msg:
                        reply = get_reply(user_msg)

                        print("BOT REPLY:", reply)

                        send_message(sender_id, reply)

    return "ok", 200

# home page display
# working 
@app.route("/")
def home():
    return "Welcome to the Facebook Messenger Bot API. Use the /webhook endpoint to connect your bot."

# favicon
@app.route("/favicon.ico")
def favicon():
    return send_from_directory("assets", "favicon.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)