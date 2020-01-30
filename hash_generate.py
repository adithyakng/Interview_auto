import pymongo
import datetime
from flask import Flask,render_template,request,jsonify,session
from flask_bcrypt import Bcrypt
from model import one_time_link as link
client = pymongo.MongoClient("mongodb+srv://dbuser:1234@cluster0-hi2xt.gcp.mongodb.net/test?retryWrites=true&w=majority")
bcrypt = Bcrypt()
app=Flask(__name__)
app.secret_key="1234"
@app.route('/',methods=['GET'])
def view_send_mail():
    return render_template('email_send.html')

@app.route('/send',methods=['POST','GET'])
def send_email():
    link.send_mail(request.json)
    return {"reply":"ok"}

@app.route('/test',methods=['GET'])
def verify():
    reply=link.verify(request.args.get("token"))
    if(reply['reply']=='ok'):
        session['username']=reply['username']
        return render_template("change_password.html",args=True)
    else:
        return render_template("fail_change.html")

@app.route('/change',methods=['GET','POST'])
def change():
    link.changePassword({'username':session['username'],'password':request.form["password"]})
    print(request.form["password"])
    return render_template('success.html')

if __name__ == "__main__":
    app.run()

    