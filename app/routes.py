from app import app, sms, twilio, allowed_users
from flask import request
import json

@app.route("/sms", methods=["GET"])
def users():
    return json.dumps(list(allowed_users.keys()))

@app.route("/sms", methods=["POST"])
def send_sms():
    r = request.json
    r = json.loads(r)
    message = r["message"]
    to = r["receipient"]

    if to in allowed_users:
        sent = sms.send(allowed_users[to], message)

        if sent:
            return "Sent"
        else:
            error = twilio(to, message)
            if error[0]:
                return "Twilio Error:\nCode %s\nMessage: %s" % (error[0], error[1])
            else:
                price = str(error[2]) + "USD" if error[2] else "free"
                return "Sent with Twilio.\nPrice: %s" % (price)
    else:
        return "You cannot send a message to this user."
