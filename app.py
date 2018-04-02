import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
item = ''

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):

    if req.get("result").get("action") == "found":

        global item

        result = req.get("result")
        parameters = result.get("parameters")
        location = parameters.get("location") 
        item = parameters.get("item")

        found_res = 'Can you help me with your personal details ? I will help you connect with the person who lost his ' + item + '.'

        # print(found_res)

        return {
            "speech": found_res,
            "displayText": found_res
        }

    elif req.get("result").get("action") == "found.found-yes":

        result = req.get("result")
        parameters = result.get("parameters")
        f_name = parameters.get("name")
        f_num = parameters.get("mobile_num")

        found_yes_res = 'Great ' + f_name + '!'+ ' Pick the ' + item + ' with you, concerned person will contact you soon :)'

        return {
            "speech": found_yes_res,
            "displayText": found_yes_res
        }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

app.run(debug=True, port=port, host='0.0.0.0')