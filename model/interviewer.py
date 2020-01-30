import pymongo
import datetime
from pymongo import WriteConcern
from pymongo import ReadPreference



client = pymongo.MongoClient("mongodb+srv://dbuser:1234@cluster0-hi2xt.gcp.mongodb.net/test?retryWrites=true&w=majority")
wc_majority = WriteConcern("majority", wtimeout=1000)


def addDate(date,time,username):
    db = client.Interviewer.slots
    db.insert_one({'name':username,'year':date[0],'month':months[date[1]],'day':date[2],'slots':time})

def interview_login(data):
    db=client.Interviewer.login
    result=db.find_one({'username':data['name']})
    if(result==None or len(result)==0):
        return False
    elif(result['password']==data['password']):
        return True
    else:
        return False

def candidate_login(data):
    db=client.login.candidate
    result=db.find_one({'username':data['name']})
    already=db.find_one({'username':data['name'],'status':'done'})
    #print(result, "bb")
    #print(already,"aa")
    print(len(result),data['name'],data['password'])
    if(len(result)==0):
        return {"reply":"wrong"}
    elif(result['password']==data['password']):
        if(already!=None and len(already)>0):
            return {"reply":"booked"}
        return {"reply":"correct"}
    else:
        return {"reply":"wrong"}
def getSlots(date):
    db=client.Interviewer.slots
    #print(date)
    reply=list(db.find({'day':date['day'],'month':date['month']}))
    #print(reply)

    for i in reply:
        del i['_id']
    
    
    return {'reply':reply}
def fixSlots(slot):
    db=client.Interviewer.slots
    #print(slot)
    reply=list(db.find({  'day':str(slot['day']),   'month':str(slot['month']),    'year':str(slot['year']),   "slots":slot['slot']   }))
    #print(reply)
    return reply
def delSlots(k,j,name):
    with client.start_session() as session:
        # client.get_database("Interviewer", write_concern=wc_majority)
        # client.get_database("login", write_concern=wc_majority)
        # s.start_transaction(read_preference=ReadPreference.PRIMARY,write_concern=wc_majority) 
        with session.start_transaction():       
            try: 
                client.Interviewer.slots.update_one( { 'name':k['name'],'day':str(j['day']),'month':str(j['month']) }, { '$pullAll': { 'slots': [ j['slot'] ] } },session=session )
                client.login.candidate.update_one({'username':name},{'$set':{'status':'done'}},session=session)
                client.Interviewer.fixed.insert_one({'i_name':k['name'],'c_username':name,'day':str(j['day']),'month':str(j['month']),'year':str(j['year']),'slot':str(j['slot'])},session=session)
                session.commit_transaction()
                session.end_session()
                print("transaction ok")
                return {'reply':'ok'}
            except Exception as e:
                print(e)
                session.abort_transaction()
                session.end_session()
                print("failure occured")
                return {'reply':'failure'}
                    

def getSlotDetails(name):
    store=client.Interviewer.fixed.find_one({'c_username':name})
    print(store," in store")
    return store


def pushDate(date):
    from_dt = date['date']
    print(from_dt)
    client.demo.test.insert_one({ from_dt:['a','b']})

 

#getSlots({'day':'21','month':'1'})
months={
    '01':'1',
    '02':'2',
    '03':'3',
    '04':'4',
    '05':'5',
    '06':'6',
    '07':'7',
    '08':'8',
    '09':'9',
    '10':'10',
    '11':'11',
    '12':'12'
}