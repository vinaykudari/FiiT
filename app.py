import urllib
import json
import os
import pandas as pd
import sqlite3 as db
from flask import Flask
from flask import request
from flask import make_response


app = Flask(__name__)

f_item = ''
f_location = ''

@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):

    if req.get("result").get("action") == "found":

        global f_item
        global f_location

        result = req.get("result")
        parameters = result.get("parameters")
        f_location = parameters.get("location") 
        f_item = parameters.get("item")

        found_res = 'Can you help me with your personal details ? I will help you connect with the person who lost his ' + f_item + '.'

        # print(found_res)

        return {
            "speech": found_res,
            "displayText": found_res
        }

    elif req.get("result").get("action") == "found.found-yes":
        
        conn = db.connect('itemdata.db')
        c = conn.cursor()

        result = req.get("result")
        parameters = result.get("parameters")
        f_name = parameters.get("name")
        f_num = parameters.get("mobile_num")

        found_yes_res = 'Great ' + f_name + '!'+ ' Pick the ' + f_item + ' with you, concerned person will contact you soon :)'
        c.execute("INSERT INTO found_items (item, f_name, f_num, f_location) values (?, ?, ?, ?)", (f_item, f_name, f_num, f_location) )
        conn.commit()
        print (pd.read_sql_query("Select * from found_items", conn))

        return {
            "speech": found_yes_res,
            "displayText": found_yes_res
        }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

app.run(debug=True, port=port, host='0.0.0.0')