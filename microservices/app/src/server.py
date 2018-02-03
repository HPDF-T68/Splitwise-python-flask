from flask import Flask, request,render_template
import requests
from flask import jsonify
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
app = Flask(__name__)
# from urllib3 import request

def email_send(toaddr,sub,body):

    fromaddr = "t68pf1@gmail.com"
    #toaddr = "manish.kumar212111@gmail.com"
    msg = MIMEMultipart()
    msg[ 'From' ] = fromaddr
    msg[ 'To' ] = toaddr
    msg[ 'Subject' ] = sub

    #body = "Manish here"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "man12345")
    text = msg.as_string()
    resp= server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return True

@app.route('/add_money_group', methods=['GET','POST'])
def add_money_group():

    content=request.get_json()
    js=json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "signup",
            "columns": [
                "money"
            ],
            "where": {
                "uid": {
                    "$eq": js['data']['uid']
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json",
         "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    data=json.loads(resp.content)
    if data[0]['money'] >= js['data']['money']:


        # This is the json payload for the query
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "group_user",
                "objects": [
                    {
                        "cash_paid": js['data']['money'],
                        "gid": js['data']['gid'],
                        "uid": js['data']['uid'],
                        "date": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str)
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

        requestPayload = {
            "type": "select",
            "args": {
                "table": "group",
                "columns": [
                    "total_expanse"
                ],
                "where": {
                    "gid": {
                        "$eq": js['data']['gid']
                    }
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        data=json.loads(resp.content)
        a=data[0]['total_expanse']+js['data']['money']

        requestPayload = {
            "type": "update",
            "args": {
                "table": "group",
                "where": {
                    "gid": {
                        "$eq": js['data']['gid']
                    }
                },
                "$set": {
                    "total_expanse": a
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        requestPayload = {
            "type": "update",
            "args": {
                "table": "signup",
                "where": {
                    "uid": {
                        "$eq": js[ 'data' ][ 'uid' ]
                    }
                },
                "$set": {
                    "money": (data['0']['money'] - js['data']['money'])
                }
            }
        }
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        # resp.content contains the json response.

        return jsonify(list=[{"message":"money added"}])



    else:
        return jsonify(list=[ {"error":"insufficient amount in account" ,"required_amount":(js['data']['money']-data[0]['money'])}])

    return resp.content
    # resp.content contains the json response.



@app.route('/add_money_account', methods=['GET','POST'])
def add_money_account():
    content=request.get_json()
    js=json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "update",
        "args": {
            "table": "signup",
            "where": {
                "uid": {
                    "$eq": js['data']['uid']
                }
            },
            "$set": {
                "money": js['data']['money']
            }
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
    return resp.content


@app.route('/list_group',  methods=['GET','POST'])
def list_group():
    content = request.get_json()
    js = json.loads(json.dumps(content))
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "group",
            "columns": [
                "gid",
                "gname"
            ],
            "where": {
                "uid": {
                    "$eq": js['data']['uid']
                }
            }
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
    return resp.content


@app.route('/list_friend',  methods=['GET','POST'])
def list_friend():
    content = request.get_json()
    js = json.loads(json.dumps(content))
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "friend",
            "columns": [
                "friend_id",
                "username"
            ],
            "where": {
                "uid": {
                    "$eq": js['data']['uid']
                }
            }
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
    return resp.content


@app.route('/create_group',  methods=['GET','POST'])
def create_group():
    content = request.get_json(force=True)
    js = json.loads(json.dumps(content))
    #return jsonify(js)
    uid=js['data']['uid']
    gname=js['data']['group_name']
    mno=js['data']['member_no']
    url = "https://data.octagon58.hasura-app.io/v1/query"
    requestPayload = {
        "type": "insert",
        "args": {
            "table": "group",
            "objects": [
                {
                    "gdate": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str),
                    "uid": uid,
                    "gname": gname,
                    "member_no": mno,

                }
                ] ,
                "returning": [
        "gid"
      ]

        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    data=json.loads(resp.content)
    assert isinstance(js, object)
    a=len(js['group_member'])
    for i in range(len(js['group_member'])):
        requestPayload = {
         "type": "insert",
            "args": {
                "table": "group_member",
                "objects": [
                    {
                        "gid":data ['returning'][0]['gid'],
                        "uid": js['group_member'][i]


                    }
                ]
            }
        }
        resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    requestPayload = {
        "type": "insert",
        "args": {
            "table": "group_user",
            "objects": [
                {
                    "gid": data[ 'returning' ][ 0 ][ 'gid' ],
                    "uid": js[ 'data' ][ 'uid' ],
                    "date": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str),

                }
            ]
        }
    }
    resp2 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    return resp.content


@app.route('/add_friend', methods=['POST'])
def add_friend():
    content = request.get_json()
    js = json.loads(json.dumps(content))

    # user authorization
    url = "https://data.octagon58.hasura-app.io/v1/query"
    requestPayload = {
            "type": "select",
            "args": {
                "table": "signup",
                    "columns": [
                    "uid",
                    "username"
                        ],
                    "where": {
                    "$or": [
                        {
                            "email": {
                                "$eq": js[ 'data' ][ 'friend_id' ]
                            }
                        },
                        {
                            "username": {
                                "$eq": js[ 'data' ][ 'friend_id' ]
                            }
                        }
                    ]
                }
             }
            }


    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
        }

        # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    data = json.loads(resp.content);
        # print data[0]['uid']
        # resp.content contains the json response.
    if not data:
        list = [
          {

                    "message": "This user does not exists"

                }
            ]
        return jsonify(resp=list)
    else:

            # This is the url to which the query is made
            url = "https://data.octagon58.hasura-app.io/v1/query"

            # This is the json payload for the query
            requestPayload = {
                "type": "insert",
                "args": {
                    "table": "friend",
                    "objects": [
                        {
                            "friend_id": data[0]['uid'] ,

                            "uid":  js['data']['uid'],
                            "username": data[0]['username']
                        }
                    ]
                }
            }

            # Setting headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
                }

            resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
            list = [
                {

                    "message": "User Added"

                }
            ]
            return jsonify(resp=list)
            # resp.content contains the json response.

    return resp.content



@app.route('/info', methods=['POST','GET'])
def info():
    content = request.get_json()


    js = json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/user/info"


    headers = {
        "Authorization": js['data']['Authorization'],
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("GET", url, headers=headers)
    data=resp.json()
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "signup",
            "columns": [
                "username"
                "email",
                "mobile",
                "currency",
                "money"
            ],
            "where": {
                "uid": {
                    "$eq": data['hasura_id']
                }
            }
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


    return resp.content

@app.route('/logout', methods=['POST'])
def logout():
    content = request.get_json()


    js = json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/user/logout"


    headers = {
        "Authorization": js['data']['Authorization'],
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
    resp1 = resp
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
                        "currency": js['data']['currency'],
                        "username": js['data']['username'],

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
        sub = "SignUp Confirmation For splitwise"
        body = " Thanks ," + js[ 'data' ][ 'username' ] + " For showing interest in us"
        email_send(js[ 'data' ][ 'email' ], sub, body)

    return resp1.content


def check_password(str):
    a = len(str)
    if a < 8:
        return False
    else:
        return True
    return True


@app.route('/login', methods=['POST'])
def login():
    content = request.get_json()
    js = json.loads(json.dumps(content))

    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/login"

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
        "Content-Type": "application/json",

    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    return resp.content


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
