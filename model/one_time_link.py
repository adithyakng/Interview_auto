import pymongo
import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
client = pymongo.MongoClient("mongodb+srv://dbuser:1234@cluster0-hi2xt.gcp.mongodb.net/test?retryWrites=true&w=majority")
bcrypt = Bcrypt()
def send_mail(data):
    db = client.demo.candidate_login
    pw_hash = bcrypt.generate_password_hash(data['username']).decode('utf-8')
    link='http://127.0.0.1:5000/test?token='+str(pw_hash)
    db.insert_one({'username':data['username'],'token':str(pw_hash),'link':link})

def verify(token):
    db=client.demo.candidate_login
    username=db.find_one({'token':token})
    print(token)
    print(username)
    if(username!=None and len(username)!=0):
        if(bcrypt.check_password_hash(token.encode(),username['username'])):
            print("matching")
            db.update_one({ "username": username['username'] },{ "$unset": {"token": ""} }  )
            return {'reply':'ok','username':username['username']}
        else:
            return {'reply':'Invalid Request or Link expired'}
    else:
        return {'reply':'invalid request'}

def changePassword(data):
    db=client.login.candidate
    print(data['password'])
    db.insert_one({'username':data['username'],'password':data['password'],'status':"pending"})