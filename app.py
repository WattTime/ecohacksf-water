from flask import Flask, g, redirect, render_template, request, session, url_for
import model
import config
import json
import os
import parser
from sqlalchemy.orm.exc import NoResultFound
import twilio
import twilio.rest

app = Flask(__name__)
app.secret_key = '\x1c][:@m\xb8\xedKt\x12x\x8a-\xaa->h\xfaH\x80=\xee\xea'#config.SECRET_KEY

@app.route("/wemo")
def hit_api():

    threshold = model.session.query(model.Threshold).filter_by(name='carbon').one()

    # hit database to get previous consumption
    try:
        previous_carbon_consumption = model.session.query(model.CarbonConsumption).one()
        has_no_previous_data = False
    
    except NoResultFound:
        has_no_previous_data = True

    # hit api to get current carbon consumption
    current_carbon = parser.hit_api()
    print current_carbon

    if has_no_previous_data == False:
        previous_carbon = previous_carbon_consumption.carbon
        print previous_carbon

        # compare against the threshold
        if current_carbon > threshold.value and previous_carbon < threshold.value:
            msg = "Turn Off"
            send_text("#off")
            # send text message to turn off
        elif current_carbon < threshold.value and previous_carbon > threshold.value:
            msg = "Turn On"
            send_text("#on")
            # send text message to turn on
        elif current_carbon > threshold.value and previous_carbon > threshold.value:
            msg = "Stay Off"

        else:
            msg = "Stay On"


        # update carbon in the database
        previous_carbon_consumption.carbon = current_carbon
        model.session.add(previous_carbon_consumption)
        model.session.commit()
        

    else:
        update_carbon = model.CarbonConsumption(carbon=current_carbon)
        model.session.add(update_carbon)
        model.session.commit()
        print "The carbon has been updated in the database."

        if current_carbon > threshold.value:
            msg = "Turn Off"
            send_text("#off")
        else:
            msg = "Turn On"
            send_text("#on")


    return json.dumps(msg)

def send_text(msg):
    wemo_phone = '+14152339406'
    WATTTIME_PHONE = '+16175534837'

    try:
        client = twilio.rest.TwilioRestClient(account = config.TWILIO_ACCOUNT_SID,
                token = config.TWILIO_AUTH_TOKEN)
        c = client.sms.messages.create(to = wemo_phone,
                from_ = WATTTIME_PHONE,
                body = msg)
        return True

    except twilio.TwilioRestException as e:
        print "Failed to send text"
        return False

if __name__ == "__main__":
    app.run()