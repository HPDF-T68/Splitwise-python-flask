from flask import Flask
import requests
from flask import jsonify
import json
from urllib3 import request
app=Flask(__name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    content = request.get_json(force=True)
      # This is the url to which the query is made

    js = json.loads(content)
    b =check_password(js['password']);
    if b == False :
        list = [
            {
                "code": "user-exists",
                "message": "Entered password must be atleast 8 digit",
                "detail": "null"
            }
        ]
        return jsonify(resp=list)



    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/signup"

    # This is the json payload for the query
    requestPayload = {
    "provider": "username",
    "data": {
        "username": js['username'],
        "password": js['password']
    }
    }

    # Setting headers
    headers = {
    "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    data=resp.json()
    if data['code'] == "user-exists":
        print "user exists"
    else:
        # This is the url to which the query is made
        url = "https://data.octagon58.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "signup",
                "objects": [
                    {
                        "uid": data['code'] ,
                        "email": js['email'],
                        "mobile": js['mobile'],
                        "currency":js['currency']
                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        # resp.content contains the json response.
        print resp.content


    return resp.content


def check_password(str):
    a=len(str)
    if a<8:
        return False
    else:
        return True
    return True


app.run(debug=True)