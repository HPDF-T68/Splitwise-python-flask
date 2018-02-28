from flask import session,Flask ,url_for, request, render_template , flash,redirect
import requests
from flask import jsonify
import json

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os

app = Flask(__name__)
    # from urllib3 import request
app.config['SESSION_TYPE'] = 'memcached'
# for image upload

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config[ 'SECRET_KEY' ] = 'jnxjasbxjsbxjhabsxhsbxjashxb'
#****************************************ALL FUNCTIONS COMES HERE

def select_friend(num):
    id=session['hasura_id']
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
                "uid": {
                    "$ne": id
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
        }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    s2 = set()
    len1 = len(resp.json())

    for i in range(0, len1):
        s2.add(resp.json()[ i ][ 'username' ])

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
                    "$eq": id
                }
            }

        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
        }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    s4 = set()

    len1 = len(resp.json())
    for i in range(0, len1):
        s4.add(resp.json()[ i ][ 'username' ])

    friend=list(s4)
    if num == 1:
        return friend
    else:
        username = list(s2 - s4)
        return username

def wallet_balance(uid):
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
                        "$eq": uid
                    }
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        if resp.json()[ 0 ][ 'money' ]:
            return resp.json()[ 0 ][ 'money' ]
        else:
            return "0"
        return "0"

def email_send(toaddr, sub, body):
        fromaddr = "t68pf1@gmail.com"
        # toaddr = "manish.kumar212111@gmail.com"
        msg = MIMEMultipart()
        msg[ 'From' ] = fromaddr
        msg[ 'To' ] = toaddr
        msg[ 'Subject' ] = sub

        # body = "Manish here"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "man12345")
        text = msg.as_string()
        resp = server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return True


def send_email_group(toaddr, sub, body):
    fromaddr = "t68pf1@gmail.com"
    # toaddr = "manish.kumar212111@gmail.com"
    msg = MIMEMultipart()
    msg[ 'From' ] = fromaddr

    msg[ 'Subject' ] = sub

    # body = "Manish here"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "man12345")
    text = msg.as_string()
    for i in toaddr:
        resp = server.sendmail(fromaddr, i, text)
    server.quit()
    return True

def group_list(uid):
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"
    a = [ ]
    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "group_member",
            "columns": [
                "gid"
            ],
            "where": {
                "uid": {
                    "$eq":uid
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    data = json.loads(resp.content)
    for i in range(len(data)):
        url = "https://data.octagon58.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "select",
            "args": {
                "table": "group",
                "columns": [
                    "gdate",
                    "gname",
                    "total_expanse",
                    "member_no",
                    "gid"
                ],
                "where": {
                    "gid": {
                        "$eq": data[ i ][ 'gid' ]
                    }
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer bbaa14a4678aa95b48f009258441ea4dd383b90231cbb544"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data1 = json.loads(resp.content)
        a.append(data1)
    session['group_list']=a
    return True

def split_bill(a):
    for i in range(0,len(a)):
        if (int(a[i]['owe'])==0  or int(a[i]['owe'])==0 ) :
            k=1;
        elif int(a[i]['owe']) > int(a[i]['owed']):
            a[i]['owe']=int(a[i]['owe'])-int(a[i]['owed'])
            a[ i ][ 'owed' ]=0
        elif int(a[i]['owe']) < int(a[i]['owed']):
            a[i]['owed']= int(a[i]['owed']) - int(a[i]['owe'])
            a[ i ][ 'owe' ]=0
        else:
            k=1

    for i in range(0,len(a)):

    # This is the url to which the query is made
        url = "https://data.octagon58.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
        "type": "update",
        "args": {
            "table": "group_user",
            "where": {
                "$and": [
                    {
                        "gid": {
                            "$eq": a[i]['gid']
                        }
                    },
                    {
                        "uid": {
                            "$eq": a[i]['uid']
                        }
                    }
                ]
            },
            "$set": {
                "owe": a[i]['owe'],
                "owed": a[i]['owed']
            }
        }
        }

        # Setting headers
        headers = {
        "Content-Type": "application/json"        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        # resp.content contains the json response.
    return resp.content
#*******************************************************************
@app.route('/invite_friend',methods=['POST','GET'])
def invite_friend():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    return render_template('invite_friend.html')

@app.route('/invite_sent',methods=['POST','GET'])
def invite_sent():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method=='POST':
        email=request.form['email']
        body="Hey "+str(session['username'])+" has invited you to join splitwise and add him as friend"
        sub="Splitwise join request"
        if email_send(email,sub,body):
            return redirect(url_for('invite_sent'))
        else:
            flash('Error occurred')
            return render_template('invite_friend.html')
    flash('Invitation sent successfully')
    return render_template('main.html')
@app.route('/refresh',methods=['POST','GET'])
def refresh():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    session.pop('group_list',None)
    group_list(session['hasura_id'])
    return render_template('main.html')

@app.route('/settle_up_group',methods=['POST','GET'])
def settle_up_group():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    gid = request.args.get('gid')
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "group",
            "columns": [
                "uid"
            ],
            "where": {
                "gid": {
                    "$eq": gid
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    if resp.json()[ 0 ][ 'uid' ] == session['hasura_id']:
        requestPayload = {
            "type": "update",
            "args": {
                "table": "group_user",
                "where": {
                    "gid": {
                        "$eq": gid
                    }
                },
                "$set": {
                    "owe": "0",
                    "owed": "0"
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        return render_template('settle_up_group.html', message="you have settled this group ")
    else:
        return render_template('settle_up_group.html',message="Only Admin Can settle Up group")

@app.route('/send_remind_group',methods=['POST','GET'])
def send_remind_group():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    gid = request.args.get('gid')

    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "group_member",
            "columns": [
                "uid"
            ],
            "where": {
                "gid": {
                    "$eq": gid
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    a = [ ]
    for i in range(0, len(resp.json())):
        a.append(resp.json()[ i ][ 'uid' ])

    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "signup",
            "columns": [
                "email"
            ],
            "where": {
                "uid": {
                    "$in": a
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    a = [ ]
    for i in range(0, len(resp.json())):
        a.append(resp.json()[ i ][ 'email' ])
    if send_email_group(a,'Splitwise Reminder','Check your splitwise account'):
        return render_template('send_remind_group.html',message='Reminder sent to everyone')
    else:
        return render_template('send_remind_group.html', message='Some problem occurs')


@app.route('/settle_up_member',methods=['POST','GET'])
def settle_up_member():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    gid = request.args.get('gid')
    uid = request.args.get('uid')
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "bulk",
        "args": [
            {
                "type": "select",
                "args": {
                    "table": "signup",
                    "columns": [
                        "email",
                        "username"
                    ],
                    "where": {
                        "uid": {
                            "$eq": uid
                        }
                    }
                }
            },
            {
                "type": "update",
                "args": {
                    "table": "group_user",
                    "where": {
                        "$and": [
                            {
                                "gid": {
                                    "$eq": gid
                                }
                            },
                            {
                                "uid": {
                                    "$eq": uid
                                }
                            }
                        ]
                    },
                    "$set": {
                        "owe": "0",
                        "owed": "0"
                    }
                }
            }
        ]
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    email_send(resp.json()[0][0]['email'],"Splitwise Notification"," "+session['username']+"  has settled you on SPLITWISE check your account")

    return render_template('settle_up_member.html',message="Settled Up successfully and reminder notification is sent",gid=gid)


@app.route('/remind_member', methods=['POST','GET'])
def remind_member():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    gid = request.args.get('gid')
    username = request.args.get('username')
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "signup",
            "columns": [
                "email",
                "uid"
            ],
            "where": {
                "username": {
                    "$eq": username
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    email=resp.json()[0]['email']


    requestPayload = {
        "type": "select",
        "args": {
            "table": "group_user",
            "columns": [
                "owed"
            ],
            "where": {
                "$and": [
                    {
                        "gid": {
                            "$eq": gid
                        }
                    },
                    {
                        "uid": {
                            "$eq": resp.json()[ 0 ][ 'uid' ]
                        }
                    }
                ]
            }
        }
    }

    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    if resp.json()[ 0 ][ 'owed' ] == 0:

        return render_template('remind_member.html',gid=gid,error="These user has already paid to this group")
    else:
        body = "Hey " + username + " Your payment is pending for you recent visit please check out Your SPLITWISE ACCOUNT"
        sub = "Payment Reminder"
        email=email
        email_send(email,sub,body)


        return render_template('remind_member.html',gid=gid,success="Reminder send successfully to this user")



@app.route('/change_group_icon',methods=['POST','GET'])
def change_group_icon():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('group_detail.html')
        file = request.files[ 'file' ]
        gid = json.loads(request.form.get('gid'))

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('group_detail.html')
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            url = "https://filestore.octagon58.hasura-app.io/v1/file/g"+str(gid)

            # This is the json payload for the query
            # Setting headers
            headers = {
                "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
            }

            # Make the query and store response in resp
            resp = requests.request("DELETE", url, headers=headers)

            # file.filename=str(session['hasura_id'])+'.jpg'
            # file.save(file.filename)
            url = "https://filestore.octagon58.hasura-app.io/v1/file/g" + str(gid)

            # Setting headers
            headers = {
                "Content-Type": "image / png",
                "Authorization": "Bearer " + session[ 'auth_token' ]
            }

            # Open the file and make the query
            # with open(file.filename, 'rb') as file_image:
            resp = requests.put(url, data=file, headers=headers)
            if "file_id" in resp.json():
                return render_template('group_icon_change.html', gid=gid,
                                       message="Profile picture changes successfully")


            else:
                return render_template('group_icon_change.html',gid=gid,fail="Profile picture change fail")

    return render_template('group_icon_change.html', fail="Profile picture change fail")


@app.route('/more_detail',methods=['POST','GET'])
def more_detail():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    gid=request.args.get('gid')
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "bulk",
        "args": [
            {
                "type": "select",
                "args": {
                    "table": "group",
                    "columns": [
                        "total_expanse",
                        "gname",
                        "gdate",
                        "member_no",
                        "gid"
                    ],
                    "where": {
                        "gid": {
                            "$eq": gid
                        }
                    }
                }
            },
            {
                "type": "select",
                "args": {
                    "table": "group_member",
                    "columns": [
                        "uid"
                    ],
                    "where": {
                        "$and": [
                            {
                                "gid": {
                                    "$eq": gid
                                }
                            },
                            {
                                "uid": {
                                    "$ne": session['hasura_id']
                                }
                            }
                        ]
                    }
                }
            }
        ]
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    ulist = [ ]
    for i in range(len(resp.json()[ 1 ])):
        ulist.append(resp.json()[ 1 ][ i ][ 'uid' ])
    # resp.content contains the json response.
    test =[]
    test.append(resp.json()[ 0 ][ 0 ])
    result1 = []

    result1.append(test)



    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "bulk",
        "args": [
            {
                "type": "select",
                "args": {
                    "table": "signup",
                    "columns": [
                        "email",
                        "username",
                        "uid"
                    ],
                    "where": {
                        "uid": {
                            "$in": ulist
                        }
                    },
                    "order_by": [
                        {
                            "column": "uid",
                            "order": "asc"
                        }
                    ]
                }
            },
            {
                "type": "select",
                "args": {
                    "table": "group_user",
                    "columns": [
                        "owe",
                        "owed",
                        "cash_paid",
                        "uid",
                        "gid"
                    ],
                    "where": {
                        "$and": [
                            {
                                "gid": {
                                    "$eq": gid
                                }
                            },
                            {
                                "uid": {
                                    "$in": ulist
                                }
                            }
                        ]
                    },
                    "order_by": [
                        {
                            "column": "uid",
                            "order": "asc"
                        }
                    ]
                }
            },
            {
                "type": "select",
                "args": {
                    "table": "group_user",
                    "columns": [
                        "owe",
                        "owed",
                        "cash_paid"
                    ],
                    "where": {
                        "$and": [
                            {
                                "gid": {
                                    "$eq": gid
                                }
                            },
                            {
                                "uid": {
                                    "$eq": session['hasura_id']
                                }
                            }
                        ]
                    }
                }
            }
        ]
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    data=json.loads(resp.content)
    result = [ ]
    for i in range(0, len(ulist)):
        c = [ resp.json()[ 0 ][ i ][ 'username' ],
              resp.json()[ 0 ][ i ][ 'email' ],
              resp.json()[ 0 ][ i ][ 'uid' ],
              resp.json()[ 1 ][ i ][ 'owe' ],
              resp.json()[ 1 ][ i ][ 'owed' ],
              resp.json()[ 1 ][ i ][ 'cash_paid' ],
              resp.json()[ 1 ][ i ][ 'gid' ] ]
        result.append(c)
    data = resp.json()
    if data:
        #return jsonify(result)
        return render_template('group_detail.html',result=result,result1=result1,result2=resp.json()[2],gid=gid)
    else:
        flash('Some error occurs')
        return render_template('main.html')

@app.route('/money_group',methods =['POST','GET'])
def money_group():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method == 'POST':
        gid=request.form['gid']
        money=request.form['money']
        uid=session['hasura_id']
        description=request.form['description']
        url = "https://data.octagon58.hasura-app.io/v1/query"
        # This is the json payload for the query
        requestPayload = {
            "type": "bulk",
            "args": [
                {
                    "type": "select",
                    "args": {
                        "table": "group",
                        "columns": [
                            "member_no",
                            "total_expanse"
                        ],
                        "where": {
                            "gid": {
                                "$eq": gid
                            }
                        }
                    }
                },
                {
                    "type": "select",
                    "args": {
                        "table": "group_member",
                        "columns": [
                            "uid"
                        ],
                        "where": {
                            "$and": [
                                {
                                    "gid": {
                                        "$eq": gid
                                    }
                                },
                                {
                                    "uid": {
                                        "$ne": uid
                                    }
                                }
                            ]
                        }
                    }
                },
                {
                "type": "update",
                        "args": {
            "table": "group",
            "where": {
                "gid": {
                    "$eq": gid
                }
            },
            "$inc": {
                "total_expanse": int(money)
            }
        }

                }
            ]
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        mno = resp.json()[ 0 ][ 0 ][ 'member_no' ]
        split = int(money) / mno

        ulist = [ ]
        for i in range(0, mno - 1):
            ulist.append(int(resp.json()[ 1 ][ i ][ 'uid' ]))
        ulistall = ulist
        ulistall.append(uid)
        url = "https://data.octagon58.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "bulk",
            "args": [
                {
                    "type": "update",
                    "args": {
                        "table": "group_user",
                        "where": {
                            "$and": [
                                {
                                    "gid": {
                                        "$eq": gid
                                    }
                                },
                                {
                                    "uid": {
                                        "$in": ulist
                                    }
                                }
                            ]
                        },
                        "$set": {},
                        "$inc": {
                            "owed": int(split)
                        }
                    },
                },
                {
                    "type": "update",
                    "args": {
                        "table": "signup",
                        "where": {
                            "uid": {
                                "$in": ulist
                            }
                        },
                        "$set": {},
                        "$inc": {
                            "owed": int(split)
                        }
                    }
                },
                {
                    "type": "update",
                    "args": {
                        "table": "signup",
                        "where": {
                            "uid": {
                                "$eq": uid
                            }
                        },
                        "$inc": {
                            "owe": int(money) - int(split)

                        }
                    }
                },
                {
                    "type": "update",
                    "args": {
                        "table": "group_user",
                        "where": {
                            "$and": [
                                {
                                    "gid": {
                                        "$eq": gid
                                    }
                                },
                                {
                                    "uid": {
                                        "$eq": uid
                                    }
                                }
                            ]
                        },
                        "$inc": {
                            "cash_paid": int(money),
                            "owe": int(money)

                        }
                    }
                },
                {
                    "type": "select",
                    "args": {
                        "table": "group_user",
                        "columns": [
                            "gid",
                            "uid",
                            "owe",
                            "owed"
                        ],
                        "where": {
                            "$and": [
                                {
                                    "gid": {
                                        "$eq": gid
                                    }
                                },
                                {
                                    "uid": {
                                        "$in": ulistall
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        result=split_bill(resp.json()[4])

        if result:
            return redirect(url_for('money_group'))
        else:
            flash('Unable to add money this time')
            return render_template('main.html')
    flash('Money addedd successfully')
    return render_template('main.html')

@app.route('/remove_friend', methods=['POST','GET'])
def remove_friend():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    username=request.args.get('username')
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "delete",
        "args": {
            "table": "friend",
            "where": {
                "$and": [
                    {
                        "username": {
                            "$eq": username
                        }
                    },
                    {
                        "uid": {
                            "$eq": session['hasura_id']
                        }
                    }
                ]
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    if resp.json()['affected_rows']:
        flash('Successfully removed'+username)
        return render_template('main.html')
    else:
        flash('Some problem occurs')
        return render_template('main.html')
    return render_template('main.html')

@app.route('/update_profile')
def update_profile():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    return render_template('update_profile.html')
@app.route('/change_profile', methods=['POST','GET'])
def change_profile():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template('update_profile.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('update_profile.html')
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            url = "https://filestore.octagon58.hasura-app.io/v1/file/"+str(session['hasura_id'])

            # This is the json payload for the query
            # Setting headers
            headers = {
            "Authorization":"Bearer bbaa14a4678aa95b48f009258441ea4dd383b90231cbb544"
            }

            # Make the query and store response in resp
            resp = requests.request("DELETE", url, headers=headers)

            #file.filename=str(session['hasura_id'])+'.jpg'
            #file.save(file.filename)
            url = "https://filestore.octagon58.hasura-app.io/v1/file/"+str(session['hasura_id'])

            # Setting headers
            headers = {
                 "Content-Type": "image / png",
                "Authorization": "Bearer bbaa14a4678aa95b48f009258441ea4dd383b90231cbb544"
            }

            # Open the file and make the query
            #with open(file.filename, 'rb') as file_image:
            resp = requests.put(url, data=file, headers=headers)

            flash('Profile picture changes successfully')
            return render_template('main.html')

        else:
            flash('Something wrong')
            return render_template('update_profile.html')
    flash('Something wrong')
    return render_template('update_profile.html')


@app.route('/update_mobile')
def update_mobile():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    return render_template('update_mobile.html')
@app.route('/change_mobile', methods=['POST','GET'])
def change_mobile():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method == 'POST':
        mobile = request.form['mobile']

        url = "https://data.octagon58.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "update",
            "args": {
                "table": "signup",
                "where": {
                    "uid": {
                        "$eq": session['hasura_id']
                    }
                },
                "$set": {
                    "mobile": mobile
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data = json.loads(resp.content)
        if "affected_rows" in data:
            flash('Updated Mobile No is :'+mobile)
            return render_template('main.html')
    flash('Some error occurs')
    return render_template('main.html')

@app.route('/update_password')
def update_password():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    return render_template('/update_password.html')
@app.route('/change_pass', methods=['POST','GET'])
def change_pass():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method == 'POST':
        new_password=request.form['new_password']
        old_password=request.form['old_password']

        url = "https://auth.octagon58.hasura-app.io/v1/providers/username/change-password"

        # This is the json payload for the query
        requestPayload = {
            "old_password": old_password,
            "new_password": new_password
        }

        # Setting headers
        headers = {
            "Authorization": "Bearer "+ session['auth_token'],
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        if resp.json()['message']=='password successfully changed':
            flash('password changed successfully')
            return render_template('main.html')
        else:
            flash('unable to change password due to internal error')
            return render_template('main.html')

    flash('some error occurs')
    return render_template('main.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make_group', methods=['POST','GET'])
def make_group():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method =='POST':
        userid=request.form.getlist("addfriend")
        gname=request.form['gname']
        uid=session['hasura_id']
        mno=len(userid)
        url = "https://data.octagon58.hasura-app.io/v1/query"
        requestPayload = {
        "type": "insert",
        "args": {
            "table": "group",
            "objects": [
                {
                    "gdate": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str),
                    "uid": session['hasura_id'],
                    "gname": gname,
                    "member_no": mno+1,

                }
            ],
            "returning": [
                "gid"
            ]

            }
        }

        headers = {
        "Content-Type": "application/json"
          }

    # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        data = json.loads(resp.content)

        b=[]
        c={"gid":data[ 'returning' ][ 0 ][ 'gid' ],"uid":uid,"gname":gname}
        b.append(c)
        for i in range(0,mno):
            c={"gid":data[ 'returning' ][ 0 ][ 'gid' ],"uid":userid[i],"gname":gname}
            b.append(c)
        d=[]
        e={ "gid": data[ 'returning' ][ 0 ][ 'gid' ],"uid": uid,"cash_paid":"00","date":json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str) ,"Description": "None","owe": "00","owed": "00"}
        d.append(e)
        for i in range(0,mno):
            e = {"gid": data[ 'returning' ][ 0 ][ 'gid' ], "uid": userid[i], "cash_paid": "00", "date": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str),  "Description": "None", "owe": "00", "owed": "00"}
            d.append(e)

        requestPayload = {
            "type": "bulk",
            "args": [
                {
                    "type": "insert",
                    "args": {
                        "table": "group_member",
                        "objects": b

                    }
                },
                {
                    "type": "insert",
                    "args": {
                        "table": "group_user",
                        "objects": d
                    }
                }
            ]
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        #data = json.loads(resp.content)
        if data[ 'returning' ][ 0 ][ 'gid' ]:
            a = group_list(session[ 'hasura_id' ])

            return redirect(url_for('make_group'))
        else:
            flash('Group Creation failed')
            return render_template('main.html',all_friend=select_friend(2))
    flash('Group Created Successfully')
    return render_template('main.html',all_friend=select_friend(2) )

@app.route('/dashboard')
def dashboard():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    return render_template('main.html',all_friend=select_friend(2))

@app.route('/main')
def main():
    if session['hasura_id']:
        return render_template('main.html')
    else:
        return render_template('login.html',message="login first")
    return render_template('login.html', message="login first")


@app.route('/update_email')
def update_email():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')
    return render_template('update_email.html')

@app.route('/change_email', methods=['POST','GET'])
def change_email():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    if request.method == 'POST':
        email=request.form['email']

        url = "https://data.octagon58.hasura-app.io/v1/query"

        # This is the json payload for the query
        requestPayload = {
            "type": "update",
            "args": {
                "table": "signup",
                "where": {
                    "uid": {
                        "$eq": session['hasura_id']
                    }
                },
                "$set": {
                    "email": email
                }
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data = json.loads(resp.content)
        if "affected_rows" in data:
            flash('Updated email id is :'+email)
            return render_template('main.html')
    flash('Some error occurs')
    return render_template('main.html')
@app.route('/add_friend_all', methods=[ 'POST', 'GET' ])
def add_friend_all():
    if 'hasura_id' not in session:
        flash('Please login first')
        return render_template('login.html')

    username=request.args.get('uname')

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

                            "username": {
                                "$eq": username
                            }


                }
            }
        }

    headers = {
            "Content-Type": "application/json"
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
        flash("Some problem occurs")
        return render_template('main.html',all_friend=select_friend(2),uid=session['hasura_id'],username=session['username'])
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
                            "friend_id": data[ 0 ][ 'uid' ],

                            "uid": session['hasura_id'],
                            "username": username
                        }
                    ]
                }
            }

        # Setting headers
        headers = {
        "Content-Type": "application/json"
        }
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        list = [
              {

                    "message": "User Added"

                }
            ]
        flash("User Added As Friend")
        return render_template('main.html',all_friend=select_friend(2),uid=session['hasura_id'],username=session['username'])
            # resp.content contains the json response.


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')
@app.route('/password_otp',methods=['POST','GET'])
def password_otp():
    if request.method=='POST':
        email=request.form['email']
        url = "https://data.octagon58.hasura-app.io/v1/query"
        requestPayload = {
            "type": "select",
            "args": {
                "table": "signup",
                "columns": [

                    "uid"
                ],
                "where": {
                    "email": {
                        "$eq": email
                    }
                }
            }
        }

        headers = {
            "Content-Type": "application/json"
        }


        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data = json.loads(resp.content);
        if not data:
            flash('Incoreect email')
            return render_template('forgot_password.html')
        else:
            toaddr=email;
            num=random.randint(1000, 9999)
            sub= 'Password Recovery OTP'
            body= ' Your SPLITWISE password recovery otp is  ' + str(num)
            email_send(toaddr, sub, body)
            session['otp']=num
            session['hasura_id']= data[ 0 ]['uid']
            return render_template('otp_send.html', email=email)
    return render_template('index.html')



    return render_template('forgot_password.html')

@app.route('/otp_verify',methods=['POST','GET'])
def otp_verify():
    if request.method=='POST':
        otp=request.form['otp']
        email=request.form['email']
        val=session['otp']
        if str(otp) == str(val):
            session.pop('otp',None)
            return render_template('password_change.html')
        else:
            flash('incorrect otp')
            return render_template('otp_send.html',email=email)
    return render_template('index.html')

@app.route('/password_change',methods=['POST','GET'])
def password_change():
    if request.method=='POST':
        password=request.form['password']
        if len(password) < 8:
            flash('pass should be of min 8 digit')
            return render_template('forgot_password.html')

        url = "https://auth.octagon58.hasura-app.io/v1/admin/user/reset-password"

        # This is the json payload for the query
        requestPayload = {
            "hasura_id": session['hasura_id'],
            "password": password
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer bbaa14a4678aa95b48f009258441ea4dd383b90231cbb544"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        if resp.json()['message']== "password updated":
            session.pop('hasura_id',None)
            flash('Password changes now signin')
            return render_template('login.html')
        else:
            flash('Error encountered')
            return render_template('index.html')


    return render_template('index.html')

@app.route('/logout_user')
def logout_user():
    if 'auth_token' in session:
        # hasura_id=request.args.get('hasura_id')
        url = "https://auth.octagon58.hasura-app.io/v1/user/logout"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + session['auth_token']
        }

        resp = requests.request("POST", url, headers=headers)
        if resp.json()['message'] ==  "logged out":
            session.pop('hasura_id', None)
            session.pop('auth_token' , None)
            session.pop('username', None)
            session.pop('all_friend',None)
            session.pop('group_list', None)
            flash('Successfully logged out')
            return render_template('index.html')
        else:
            flash('Please Login First')
            return render_template('login.html')
    flash('invalid session')
    return redirect(url_for("index"))


@app.route('/register', methods=[ 'POST' , 'GET' ])
def register():
    return render_template('register.html')


@app.route('/signup_submit', methods=[ 'POST', 'GET' ])
def signup_submit():
    if request.method == 'POST':
        username = request.form[ 'username' ]
        email = request.form[ 'email' ]
        mobile = request.form[ 'mobile' ]
        password = request.form[ 'password' ]
        url = "https://data.octagon58.hasura-app.io/v1/query"
        requestPayload = {
            "type": "select",
            "args": {
                "table": "signup",
                "columns": [
                    "email"
                ],
                "where": {

                    "email": {
                        "$eq": email
                    }

                }
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        if len(resp.json()) != 0:
            flash('Email already registered')
            return render_template('register.html', email=email, mobile=mobile, username=username)

        url = "https://app.octagon58.hasura-app.io/signup"

        # This is the json payload for the query
        requestPayload = {
            "data": {
                "username": username,
                "email": email,
                "mobile": mobile,
                "password": password,
                "currency": "INR"

            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data = json.loads(resp.content)
        if 'hasura_id' in resp.json():
            session[ 'auth_token' ] = resp.json()[ 'auth_token' ]
            session[ 'hasura_id' ] = resp.json()[ 'hasura_id' ]
            session[ 'username' ] = resp.json()[ 'username' ]
            session[ 'all_friend' ] = select_friend(2)
            return render_template('main.html')

        if resp.json()['code']== "user-exists":
            flash('Username Exists Plzz change')
            return render_template('register.html',email=email,mobile=mobile,username=username)
        else:
            flash('min password len 8 digit')
            return render_template('register.html', email=email, mobile=mobile)


    return render_template('index.html')


@app.route('/login_form', methods=[ 'POST', 'GET' ])
def login_form():
    return render_template('login.html')


@app.route('/login_submit', methods=[ 'POST', 'GET' ])
def login_submit():

    if request.method == 'POST':

        username = request.form[ 'username' ]
        password = request.form[ 'password' ]

        url = "https://app.octagon58.hasura-app.io/login"

        # This is the json payload for the query
        requestPayload = {
            "data": {
                "username": username,
                "password": password
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json",
        }

        # Make the query and store response in resp
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        # data=json.loads(resp.content)
        if 'hasura_id' in resp.json():
            a=group_list(resp.json()['hasura_id'])
            session['auth_token'] = resp.json()['auth_token']
            session['hasura_id'] = resp.json()['hasura_id']
            session[ 'username' ] = resp.json()[ 'username' ]
            session[ 'all_friend' ] = select_friend(2)

            return redirect(url_for('login_submit'))
        else:
            flash('Please Check username or password')
            return render_template('login.html', username=username)
    return render_template('main.html')

@app.route('/add_money_group', methods=[ 'GET', 'POST' ])
def add_money_group():
    content = request.get_json()
    js = json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"


    # This is the json payload for the query
    requestPayload = {
            "type": "insert",
            "args": {
                "table": "group_user",
                "objects": [
                    {
                        "cash_paid": js[ 'data' ][ 'money' ],
                        "gid": js[ 'data' ][ 'gid' ],
                        "uid": js[ 'data' ][ 'uid' ],
                        "date": json.dumps(datetime.date.today(), indent=4, sort_keys=True, default=str),
                        "Description":js['data']['description']
                    }
                ]
            }
        }

    # Setting headers
    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
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
                        "$eq": js[ 'data' ][ 'gid' ]
                    }
                }
            }
    }

    # Setting headers
    headers = {
            "Content-Type": "application/json",
             "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)


    data = json.loads(resp.content)

    a = data[0]['total_expanse'] + js[ 'data' ][ 'money' ]

    requestPayload = {
        "type": "update",
        "args": {
                "table": "group",
                "where": {
                    "gid": {
                        "$eq": js[ 'data' ][ 'gid' ]
                    }
                },
                "$set": {
                    "total_expanse": a
                }
            }
        }

    # Setting headers
    headers = {
            "Content-Type": "application/json"
        }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)


    return resp.content
        # resp.content contains the json response.


@app.route('/add_money_account', methods=[ 'GET', 'POST' ])
def add_money_account():
    content = request.get_json()
    js = json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
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
                "money": js[ 'data' ][ 'money' ]
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


@app.route('/list_group', methods=[ 'GET', 'POST' ])
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
                    "$eq": js[ 'data' ][ 'uid' ]
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    return resp.content


@app.route('/list_friend', methods=[ 'GET', 'POST' ])
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
                    "$eq": js[ 'data' ][ 'uid' ]
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    return resp.content


@app.route('/create_group', methods=[ 'GET', 'POST' ])
def create_group():
    content = request.get_json(force=True)
    js = json.loads(json.dumps(content))
    # return jsonify(js)
    uid = js[ 'data' ][ 'uid' ]
    gname = js[ 'data' ][ 'group_name' ]
    mno = js[ 'data' ][ 'member_no' ]
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
            ],
            "returning": [
                "gid"
            ]

        }
    }

    headers = {
        "Content-Type": "application/json"    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    data = json.loads(resp.content)
    assert isinstance(js, object)
    a = len(js[ 'group_member' ])
    for i in range(len(js[ 'group_member' ])):
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "group_member",
                "objects": [
                    {
                        "gid": data[ 'returning' ][ 0 ][ 'gid' ],
                        "uid": js[ 'group_member' ][ i ],
                        "gname":gname

                    }
                ]
            }
        }
        resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    requestPayload = {
        "type": "insert",
        "args": {
            "table": "group_member",
            "objects": [
                {
                    "gid": data[ 'returning' ][ 0 ][ 'gid' ],
                    "uid": uid

                }
            ]
        }
    }
    resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    # resp.content contains the json response.
    return resp.content


@app.route('/add_friend', methods=[ 'POST' ,'GET'])
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
        "Content-Type": "application/json"    }

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
                        "friend_id": data[ 0 ][ 'uid' ],

                        "uid": js[ 'data' ][ 'uid' ],
                        "username": data[ 0 ][ 'username' ]
                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
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


@app.route('/info', methods=[ 'POST', 'GET' ])
def info():
    content = request.get_json()

    js = json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/user/info"
    a=js[ 'data' ][ 'Authorization' ]
    headers = {
        "Authorization": a,
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("GET", url, headers=headers)
    data = resp.json()
    # This is the url to which the query is made
    url = "https://data.octagon58.hasura-app.io/v1/query"

    # This is the json payload for the query
    requestPayload = {
        "type": "select",
        "args": {
            "table": "signup",
            "columns": [
                "uid",
                "username",
                "email",
                "mobile"
            ],
            "where": {
                "uid": {
                    "$eq": resp.json()['hasura_id']
                }
            }
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"}

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    return resp.content


@app.route('/logout', methods=[ 'POST', 'GET' ])
def logout():
    content = request.get_json()

    js = json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/user/logout"

    headers = {
        "Authorization": js[ 'data' ][ 'Authorization' ],
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, headers=headers)

    # resp.content contains the json response.
    return resp.content


@app.route('/signup', methods=[ 'POST', 'GET' ])
def signup():
    content = request.get_json()
    # content = request.json
    # This is the url to which the query is made

    js = json.loads(json.dumps(content))
    b = check_password(js[ 'data' ][ 'password' ])
    if not b:
        list = {
          "data":  {
                "code": "error",
                "message": "Entered password must be atleast 8 digit",
                "detail": "null"
            }
        }
        return jsonify(resp=list)

    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/signup"

    # This is the json payload for the query
    requestPayload = {
        "provider": "username",
        "data": {
            "username": js[ 'data' ][ 'username' ],
            "password": js[ 'data' ][ 'password' ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    resp1 = resp
    # data = json.dumps(resp)
    # data= resp.json()
    # if 'This user already exists' != resp.json()['message']:
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
                        "uid": resp.json()[ 'hasura_id' ],
                        "email": js[ 'data' ][ 'email' ],
                        "mobile": js[ 'data' ][ 'mobile' ],
                        "currency": js[ 'data' ][ 'currency' ],
                        "username": js[ 'data' ][ 'username' ],

                    }
                ]
            }
        }

        # Setting headers
        headers = {
            "Content-Type": "application/json"
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


@app.route('/login', methods=[ 'POST', 'GET' ])
def login():
    content = request.get_json()
    js = json.loads(json.dumps(content))

    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/login"

    # This is the json payload for the query
    requestPayload = {
        "provider": "username",
        "data": {
            "username": js[ 'data' ][ 'username' ],
            "password": js[ 'data' ][ 'password' ]
        }
    }

    # Setting headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    return resp.content


if __name__ == '__main__':

    app.run(debug=True)
