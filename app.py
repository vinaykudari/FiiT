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
    print(res)
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

    elif req.get("result").get("action") == "lost":

        conn = db.connect('itemdata.db')
        c = conn.cursor()
        temp = ''

        result = req.get("result")
        parameters = result.get("parameters")
        l_location = parameters.get("location") 
        l_item = parameters.get("item")

        query = "SELECT f_name, f_num from found_items where item = '" + l_item + "' AND f_location = '" + l_location + "'"
        query_count = "SELECT COUNT(*) FROM (" + query + ")"

        query_res = pd.read_sql_query(query, conn)
        query_res_count = pd.read_sql_query(query_count, conn)

        print(query_res)

        lost_not_found = 'Sorry the ' + l_item + ' wasnt reported to be found yet, Please check again after a while :)'
        lost_found = str(query_res_count.iloc[0]['COUNT(*)']) + ' people reported that they found ' + l_item + ' near ' + l_location + '. Here are the details \n'

        for i in range(query_res_count.iloc[0]['COUNT(*)']):
            temp = temp + (query_res.iloc[i]['f_name'] + "   " + query_res.iloc[i]['f_num'] + "  \n")
            
        web_res = lost_found + temp

        if(query_res.empty):

            return {
                "speech": lost_not_found,
                "displayText": lost_not_found
            }

        else:
            return {
                    "speech" : web_res,
                    "messages" : [
                        {
                            "type" : 0,
                            "speech" : lost_found
                        },
                        {
                            "type" : 0,
                            "speech" : temp
                        }
                    ]
            }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

app.run(debug=True, port=port, host='0.0.0.0')