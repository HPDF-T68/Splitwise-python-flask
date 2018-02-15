from flask import session,Flask ,url_for, request, render_template , flash,redirect
import requests
from flask import jsonify
import json
from flask_debugtoolbar import DebugToolbarExtension
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
app.config['DEBUG']=True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
toolbar=DebugToolbarExtension(app)


@app.route('/remove_friend', methods=['POST','GET'])
def remove_friend():
    username=request.args.get('username')



@app.route('/update_profile')
def update_profile():
    return render_template('update_profile.html')
@app.route('/change_profile', methods=['POST','GET'])
def change_profile():
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

            #file.filename=str(session['hasura_id'])+'.jpg'
            #file.save(file.filename)
            url = "https://filestore.octagon58.hasura-app.io/v1/file/"+str(session['hasura_id'])

            # Setting headers
            headers = {
                 "Content-Type": "image / png",
                "Authorization": "Bearer "+session['auth_token']
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
    return render_template('update_mobile.html')
@app.route('/change_mobile', methods=['POST','GET'])
def change_mobile():
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
            "Content-Type": "application/json",
            "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
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
    return render_template('/update_password.html')
@app.route('/change_pass', methods=['POST','GET'])
def change_pass():
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
        "Content-Type": "application/json",
        "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
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
        "Content-Type": "application/json",
        "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
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

@app.route('/make_group', methods=[ 'GET', 'POST' ])
def make_group():

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
                    "member_no": mno,

                }
            ],
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

        data = json.loads(resp.content)
        requestPayload = {
            "type": "insert",
            "args": {
                "table": "group_member",
                "objects": [
                    {
                        "gid": data[ 'returning' ][ 0 ][ 'gid' ],
                        "uid": uid,
                        "gname": gname

                    }
                ]
            }
        }
        resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

        for i in range(0,mno):

            requestPayload = {
            "type": "insert",
            "args": {
                "table": "group_member",
                "objects": [
                    {
                        "gid": data[ 'returning' ][ 0 ][ 'gid' ],
                        "uid": userid[i],
                        "gname":gname

                    }
                ]
                }
                }
            resp1 = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        data = json.loads(resp1.content)
        if "affected_rows" in data:
            flash('Group Created successfully')
            return render_template('main.html', all_friend=select_friend(2))
        else:
            flash('Group Creation failed')
            return render_template('main.html', all_friend=select_friend(2))
    return render_template('main.html', all_friend=select_friend(2))

@app.route('/dashboard')
def dashboard():
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
    return render_template('update_email.html')

@app.route('/change_email', methods=['POST','GET'])
def change_email():
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
            "Content-Type": "application/json",
            "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
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
        "Content-Type": "application/json",
            "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
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
            "Content-Type": "application/json",
            "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
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
            "Authorization": "Bearer c6fd65b8291402d919b7e940069cdd655109daa75b970967"
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
            session['auth_token'] = resp.json()['auth_token']
            session['hasura_id'] = resp.json()['hasura_id']
            session[ 'username' ] = resp.json()[ 'username' ]
            session[ 'all_friend' ] = select_friend(2)
            return render_template('main.html')
        else:
            flash('Please Check username or password')
            return render_template('login.html', username=username)
    return redirect(url_for("index"))


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


@app.route('/add_money_group', methods=[ 'GET', 'POST' ])
def add_money_group():
    content = request.get_json()
    js = json.loads(json.dumps(content))
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
                    "$eq": js[ 'data' ][ 'uid' ]
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
    data = json.loads(resp.content)
    b = data[ 0 ][ 'money' ]
    c = js[ 'data' ][ 'money' ]
    if data[ 0 ][ 'money' ] >= js[ 'data' ][ 'money' ]:

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
                        "$eq": js[ 'data' ][ 'gid' ]
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

        data = json.loads(resp.content)
        a = data[ 0 ][ 'total_expanse' ] + js[ 'data' ][ 'money' ]

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
                    "money": b - c
                }
            }
        }
        resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
        # resp.content contains the json response.

        return jsonify(list=[ {"message": "money added"} ])



    else:
        return jsonify(list=[ {"error": "insufficient amount in account",
                               "required_amount": (js[ 'data' ][ 'money' ] - data[ 0 ][ 'money' ])} ])

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
        "Content-Type": "application/json",
        "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
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
        "Content-Type": "application/json",
        "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
    }

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
        "Content-Type": "application/json",
        "Authorization": "Bearer b660de1696fbdc8daa1d32d1d8f19bf03315ec407b9e2ebf"
    }

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
                        "friend_id": data[ 0 ][ 'uid' ],

                        "uid": js[ 'data' ][ 'uid' ],
                        "username": data[ 0 ][ 'username' ]
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


@app.route('/info', methods=[ 'POST', 'GET' ])
def info():
    content = request.get_json()

    js = json.loads(json.dumps(content))
    # This is the url to which the query is made
    url = "https://auth.octagon58.hasura-app.io/v1/user/info"

    headers = {
        "Authorization": js[ 'data' ][ 'Authorization' ],
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
                "username"
                "email",
                "mobile",
                "currency",
                "money"
            ],
            "where": {
                "uid": {
                    "$eq": data[ 'hasura_id' ]
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
        "Content-Type": "application/json",

    }

    # Make the query and store response in resp
    resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)

    return resp.content


if __name__ == '__main__':

    app.run(debug=True)
