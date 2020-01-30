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
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = '123asdiahjshdjashdkja123' 

jwt = JWTManager(app)


@app.route('/',methods=['GET','POST'])
def function():
    return render_template('login.html')



@app.route('/int_login',methods=['GET'])
def view_page():
    return render_template('login.html')

@app.route('/validate',methods=['POST'])
def interviewer_login():
    data=request.json
    flag=inter.interview_login(data)
    if(flag==True):
        reply="success"
        session['username']=data['name']
    else: 
        reply="fail"
    return {'reply':reply}

@app.route('/getSlots',methods=['POST'])
def getSlots():
    data=request.json
    print(data)
    slots=inter.getSlots(data)
    
   # print(slots)
    return {'reply':slots['reply']}

@app.route('/assign_slot',methods=['POST','GET'])
def assign_slot():
    picked_slots=request.json
    for i in range(len(picked_slots)):
        reply=inter.fixSlots(picked_slots[i])
        print(reply)
        if(len(reply)>=1):
            min=0
            max=len(reply)-1
            r_num=random.randint(min,max)
            print("adithya\n")
            print(reply[r_num], "adithya is great")
            reply1=inter.delSlots(reply[r_num],picked_slots[i],session['username'])
            if(reply1['reply']=='fail'):
                continue
            elif(reply1['reply']=='ok'):
                del reply[r_num]['_id']
                del reply[r_num]['slots']
                session['date']=reply[r_num]
                session['slot']=picked_slots[i]['slot']
                return {"reply":reply[r_num],"slot":picked_slots[i]['slot']}
    return {"reply":"fail"}
        
    

@app.route('/cal',methods=['GET','POST'])
@jwt_required
def calender():
    return render_template('calender.html')

@app.route('/slot_details',methods=['GET','POST'])
@jwt_required
def show_slot_details():
    sendmail(session["username"],session["username"])
    resp = jsonify({'refresh': True})
    unset_jwt_cookies(resp)
    res=make_response(render_template('slot_details.html'))
    res.set_cookie('access_token_cookie',"",max_age=0) 
    return res

@app.route('/show_details',methods=['GET','POST'])
def show_details():
    a=session['date']
    b=session['slot']
    
    return {"reply":a,"slot":b}

@app.route('/slot_fail',methods=['GET','POST'])
@jwt_required
def failure():
    return render_template('slot_fail.html')

@app.route('/cand_login',methods=['GET','POST'])
def cand_login():
    data=request.json
    flag=inter.candidate_login(data)
    session["username"]=data['name']
    print(flag,data['name'])
    if(flag['reply']=="wrong"):
        return jsonify({'reply': False})
    if(flag['reply']=="booked"):
        return jsonify({'reply':'booked'})
    access_token = create_access_token(identity=data['name'])
    refresh_token = create_refresh_token(identity=data['name'])
    resp = jsonify({'reply': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp
    #db.send_mail(request.json)
    



    # Create the tokens we will be sending back to the user
   

    # Set the JWTs and the CSRF double submit protection cookies
    # in this response
        
        # reply="success"
        # session['username']=data['name']

@app.route('/cand_login_page',methods=['GET'])
def cand_login_page():
    return render_template('cand_login.html')



def sendmail(name,mailid):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    print(name,mailid)
    s.starttls()
    s.login("shiva.darwinbox@gmail.com", "Abcd@1234")
    m="""Thank you for booking your slot"""
    message="\nYour Slot details are as follows \n"
    day=session["date"]['day']
    month=session["date"]['month']
    year=session["date"]["year"]
    slot=session['slot']
    slot_message="DATE: "+day+"/"+month+"/"+year+" at "+slot+"\n MAKE SURE THAT YOU ARE AVAILABLE AS PER YOUR SLOT."
    message=m+message+slot_message
    print(str(message))
    s.sendmail("shiva.darwinbox@gmail.com", mailid, message)
    print("DONE")
    s.quit()



@app.route('/demo',methods=['POST','GET'])
def some_func():
    inter.pushDate(request.json)
    return render_template("login.html")

@app.route('/view')
def view():
    return render_template("test.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0")



# @app.route('/token/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     # Create the new access token
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)

#     # Set the access JWT and CSRF double submit protection cookies
#     # in this response
#     resp = jsonify({'refresh': True})
#     set_access_cookies(resp, access_token)
#     return resp, 200


# # Because the JWTs are stored in an httponly cookie now, we cannot
# # log the user out by simply deleting the cookie in the frontend.
# # We need the backend to send us a response to delete the cookies
# # in order to logout. unset_jwt_cookies is a helper function to
# # do just that.
# @app.route('/token/remove', methods=['POST'])
# def logout():
#     resp = jsonify({'logout': True})
#     unset_jwt_cookies(resp)
#     return resp, 200


# @app.route('/api/example', methods=['GET'])
# @jwt_required
# def protected():
#     username = get_jwt_identity()
#     return jsonify({'hello': 'from {}'.format(username)}), 200


# @app.route('/booked',methods=['GET','POST'])
# def booked_status():
#     print("HI")
#     getDetails=inter.getSlotDetails(session['username'])
#     print(getDetails)
#     print("In booked")
#     session['date']={'day':getDetails['day'],'month':getDetails['month'],'year':getDetails['year']}
#     session['slot']=getDetails['slot']
#     print("success")
#     return {'reply':session['date'],'slot':session['slot']}