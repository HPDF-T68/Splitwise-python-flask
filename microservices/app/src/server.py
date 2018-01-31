from flask import Flask, request
import requests
from flask import jsonify
import json

# from urllib3 import request
app = Flask(__name__)
@app.route('/logout', methods=['POST'])
def logout():

    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/user/logout"
    r = requests.get('https://app.octagon58.hasura-app.io/logout')
    # This is the json payload for the query
    a=r.headers['Authorization']
    # Setting headers
    #a='Bearer '+ a;
    headers = {
        "Authorization": a,
        "Content-Type": "application/json"
    }

# Make the query and store response in resp
    resp = requests.request("POST", url, headers=headers)

# resp.content contains the json response.
    return resp.content

@app.route('/signup', methods=['POST'])
def signup():
    content = request.get_json()
    #content = request.json
    #This is the url to which the query is made

    js = json.loads(json.dumps(content))
    b = check_password(js['data']['password'])
    if not b:
        list = [
            {
                "code": "error",
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
            "username": js['data']['username'],
            "password": js['data']['password']
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    resp1-resp
    #data = json.dumps(resp)
    #data= resp.json()
    #if 'This user already exists' != resp.json()['message']:
    if "hasura_id" in resp.json():



        # This is the url to which the query is made
        url = "https://data.octagon58.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "signup",
                "objects": [
                    {
                        "uid": resp.json()['hasura_id'],
                        "email": js['data']['email'],
                        "mobile": js['data']['mobile'],
                        "currency": js['data']['currency']
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
        # print resp.content

    return resp1.content


def check_password(str):
    a = len(str)
    if a < 8:
        return False
    else:
        return True
    return True


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
