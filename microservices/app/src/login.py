from flask import Flask
import requests
import json
from urllib3 import request
app=Flask(__name__)

@app.route('/login', methods=['POST'])
def signup():
    content = request.get_json(force=True)
      # This is the url to which the query is made

    js = json.loads(content)

    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/login"

    # This is the json payload for the query
    requestPayload = {
        "provider": "username",
        "data": {
            "username": js['username'],
            "password": js['username']
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",

    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    data = resp.json()
    hasura_id=data['hasura_id']
    # resp.content contains the json response.
    #print resp.content
    return resp.content
if __name__ == '__main__':
    app.run(debug=True)