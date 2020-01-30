from flask import Flask,request,jsonify,render_template,session,Response,make_response
from model import interviewer as inter
import random
import smtplib
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

app=Flask(__name__)
app.secret_key='1234'

# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = False

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# Enable csrf double submit protection. See this for a thorough
# explanation: http://www.redotheweb.com/2015/11/09/api-security.html
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = '123asdiahjshdjashdkja123'  # Change this!

jwt = JWTManager(app)


@app.route('/',methods=['GET','POST'])
def function():
    return render_template('login.html')

@app.route('/validate',methods=['POST'])
def interviewer_login():
    data=request.json
    flag=inter.interview_login(data)
    if(flag==True):
        session['username']=data['name']
        access_token = create_access_token(identity=data['name'])
        refresh_token = create_refresh_token(identity=data['name'])
        resp = jsonify({'reply': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp
    else: 
        return {'reply':False}
@app.route('/slot_fix',methods=['GET'])
@jwt_required
def fix_slots():
    return render_template('basic.html')

@app.route('/logout',methods=['POST'])
@jwt_required
def logout():
    resp = jsonify({'refresh': True})
    unset_jwt_cookies(resp)
    res=make_response(render_template("dummy.html"))
    res.set_cookie('access_token_cookie',"",max_age=0) 
    return res


@app.route('/todb',methods=['POST'])
def toDB():
    data=request.json
    date=data['date'].split("-")
    inter.addDate(date,data['time'],session['username'])
    print(date)
    return {'reply':'success'}

if __name__ == "__main__":
    app.run(debug=True)
    
    