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

    try:
        message = r["message"]
        receipients = r["receipients"]
        if type(receipients) == str: receipients = [receipients]
        receipients = list(set(receipients)) # remove duplicates
        if not (receipients and message): raise KeyError # if the value of message or receipients is empty
    except KeyError:
        return "Your API call is not valid."

    sent, twilio_sent, twilio_errors, errors = list(), list(), list(), list()
    for receipient in receipients:
        if receipient in allowed_users:
            success = sms.send(allowed_users[receipient], message)

            if success:
                sent.append(receipient)
            else:
                error = twilio(receipient, message)
                if error[0]:
                    twilio_errors.append((receipient, error[0], error[1]))
                else:
                    twilio_sent.append(receipient)
        else:
            errors.append(receipient)

    output = dict()
    if sent:
        output["sent"] = sent
    if twilio_sent:
        output["twilio_sent"] = twilio_sent
    if twilio_errors:
        output["twilio_errors"] = {e[0]:(e[1], e[2]) for e in twilio_errors}
    if errors:
        output["errors"] = errors

    return json.dumps(output)
