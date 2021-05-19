from flask import Flask,render_template,request,make_response,session
from time import time
import json
from flask_sqlalchemy import SQLAlchemy
from newspaper import Article
import random
import string
from random import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
from datetime import date





###.....Flask App...####
app=Flask(__name__)
app.secret_key= "wikedcase"



####....Database...#####
ENV='dev'


if ENV =='dev':
    app.debug=True
    #psycopg2.connect(database="netscore",user="postgres",password="r@ms@i143",host="localhost")
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:r@ms@i143@localhost/netscore'
    #app.config['SQLALCHEMY_BINDS']={'two':'postgresql://postgres:r@ms@i143@localhost/NetTrucks'}
    
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']='postgres://fvqetjhrvrpxhr:ce042368affc2747c475683a4669dedbd9d807a6090d12c902a8521e2122d259@ec2-54-211-77-238.compute-1.amazonaws.com:5432/ddkfcsgkpatpg7'

#app.config['SQLALCHEMY_TRACK_MODIFICATION']=False


#####...............Connecting to Database..........##########
db= SQLAlchemy(app)

class Check(db.Model):
    __tablename__='Login_Details'
    id=db.Column(db.Integer, primary_key=True)
    firstname=db.Column(db.String(200))
    lastname=db.Column(db.String(200))
    email=db.Column(db.String(200))
    password=db.Column(db.String(200))
    #cpid=db.Column(db.Integer)
    per=db.Column(db.String(200))

#bd=SQLAlchemy(app)

class Bot(db.Model):
    #__bind_key__='two'
    __tablename__='Truck_Details'
    id=db.Column(db.Integer, primary_key=True)
    truckname=db.Column(db.String(200))
    truckno=db.Column(db.String(200))
    loadcapicty=db.Column(db.String(200))
    maxload=db.Column(db.String(200))
    uname=db.Column(db.String(200))
    










#login page
@app.route('/',methods=['GET','POST'])

def fun():
    return render_template('my.html')

@app.route('/sai/',methods=['GET','POST'])
def fun2():
    session['name']=request.form['nam']
    name=session['name']
    password=request.form['pass']
    cd='wrong email or password'
    data=Check.query.filter(Check.email==name)
    fill=Check.query.filter(Check.password==password)
    dc=[]
    op=[]
    for j in fill:
        check={}
        check['email']=j.email
        check['password']=j.password
        dc.append(check)
    for i in data:
        form={}
        form['email']=i.email
        form['password']=i.password
        op.append(form)
    if bool(op)==True and bool(dc)==True:
        return render_template('mainpage.html',si='{}'.format(name))    
        
    return render_template('my.html',ds='{}'.format(cd))

#register form and saving to data base
@app.route('/ram/',methods=['GET','POST'])
def fun3():
    return render_template('sign.html')

@app.route('/snv/',methods=['GET','POST'])
def fun4():
   firstname=request.form['fir']
   lastname=request.form['lst']
   email=request.form['em']
   password=request.form['pass']
   vrpass=request.form['vpass']
   per=request.form['opttick']
   cpid=request.form['cid']
   
   dp='password unmatched'
   if password==vrpass and per=='personal':
       data=Check(firstname=firstname,lastname=lastname,email= email,password=password,per=per)
       db.session.add(data)
       db.session.commit()
        

   else:
       return render_template('sign.html',cc='{}'.format(dp))
   


   return render_template('my.html')
@app.route('/graphs/',methods=['GET','POST'])
def fun5():
    return render_template('live.html')
    
############new code starts###############
import json
from sseclient import SSEClient 
import pandas as pd
def func(dic):
    re ={}
    for k,v in dic.items():
        if isinstance(v, dict):
            re.update(v)
        else:
            re.update({k:v})
    return re
messages = SSEClient('https://api.particle.io/v1/products/tracker-one-12878/events?access_token=537b673970bf891455e3a702bbac704166e6ce8f')
# for msg in messages:
    #prior code omitted from this post cleanliness
    
def data():
    for msg in messages:
    
    #Get the message event type. This is the Publish Event name. 
        event = str(msg.event)

 

    #Only add events to SQL that have the event name of "Stat"
        if event == 'loc-enhanced':
            data = str(msg.data)
            msgDict = json.loads(data)
            dataDict = json.loads(msgDict["data"])
            dfr=(func(dataDict))
            ch=dfr['spd']
            return ch




#this analytics graphs...
@app.route('/live-data')
def live_data():
    for i in range(100):
        cha=[data()]
        response = make_response(json.dumps(cha))
        response.content_type = 'application/json'
        return response
    # Create a PHP array and echo it as JSON
    #data = [time() * 1000,random() * 100]
    

#####################code ends ##########################
#getting devices page ...
@app.route('/getdev/',methods=['GET','POST'])
def fun6():
    return render_template('devices1.html')
#this function  are device data....
@app.route('/tees/',methods=['GET','POST'])
def fun7():
    if 'name' in session:
        df=session['name']

        fd='123432'
        dg='B Series LTE CAT1/3G/2G'
        sd='Tracking device'
        return render_template('mainpage.html',cg='{}'.format(fd),kl='{}'.format(sd),fd='{}'.format(dg),si='{}'.format(df))

@app.route('/tee/',methods=['GET','POST'])
def fun8():
    if 'name' in session:
        df=session['name']
        fd='123432'
        dg='B Series LTE CAT1/3G/2G'
        sd='Tracking device'
        return render_template('mainpage.html',ss='{}'.format(fd),sss='{}'.format(sd),ssss='{}'.format(dg),si='{}'.format(df))



@app.route('/act/',methods=['GET','POST'])
def fun9():
    name=session['name']
    
    session['tname']=request.form['usr1']
    tname=session['tname']
    tno=request.form['usr2']
    lcap=request.form['usr3']
    mload=request.form['usr4']
    uvname=session['name']
    data=Bot(truckname=tname,truckno=tno,loadcapicty=lcap,maxload=mload,uname=uvname)
    db.session.add(data)
    db.session.commit()
    # #sensor1=request.form['op1']
    #sensor2=request.form['op2']
    #sensor3=request.form['op3']
    #sensor4=request.form['op4']
    #print(sensor1)
    #print(sensor2)
    #print(sensor3)
    #print(sensor4)
    return render_template('mainpage.html',si='{}'.format(name))

@app.route('/act1/',methods=['GET','POST'])

def Truck():
    temp=session['name']
    tech=Bot.query.filter(Bot.uname==temp).all()
    xtname=[]
#query for getting objects
    tech=Bot.query.filter(Bot.uname==temp).all()
    image_dict = []
    for j in tech:
        image_history = dict({
        "type": j.truckname,
        "timestamp": j.truckno,
        "loadcap":j.loadcapicty,
     })
        image_dict.append(image_history)
    #print(image_dict)

    return render_template('trucks.html',name1=image_dict,jlm=temp)
           


@app.route('/main/',methods=['GET','POST'])

def mainpage():
    today = date.today()
    d4 = today.strftime("%b-%d-%Y")
    name=session['name']
    return render_template('mainpage.html',si='{}'.format(name),mim='{}'.format(d4))

@app.route('/mnd/',methods=['GET','POST'])

def database():
    return render_template('sign.html')

#.................chart bot...........#

#download punkt package
nltk.download('punkt',quiet=True)

#get the article
article=Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
#import pandas as pd
#df=pd.read_csv('D:\sairam/netsuitex.csv')
article.download()
article.parse()
article.nlp()
corpus=article.text

#Tokenization
text=corpus
sentence_list=nltk.sent_tokenize(text)


@app.route('/gets',methods=['GET','POST'])
def chart():
    
    #print('hi')
    #print('welcome*******')
    a=request.args.get('msg')
    #print(a)
    #return "hello world"
    exit_list=['bye','see u later','exit','thanks']
    wel_list=['hi']
    while(True):
        user_input=a
        if user_input.lower() in exit_list or user_input.lower() in wel_list:
            return str(user_input)
        else:
                #print('hi')
            if bot_response(user_input) != None:
                d=bot_response(user_input)
                    #print(d)
                return str(d)




def bot_response(user_input):
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_response=''
    cm=CountVectorizer().fit_transform(sentence_list)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    index=index[1:]
    response_flag=0

    j=0

    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response=bot_response+' '+sentence_list[index[i]]
            response_flag=1
            j=j+1
        if j>2:
           break
    if response_flag == 0:
       bot_response=bot_response+' '+"sorry!,Idon't understant."
    
    sentence_list.remove(user_input)
    
    return bot_response

def index_sort(list_var):
   length=len(list_var)
   list_index=list(range(0,length))
   x=list_var
   for i in range(length):
       for j in range(length):
           if x[list_index[i]] > x[list_index[j]]:
                                   temp=list_index[i]
                                   list_index[i]=list_index[j]
                                   list_index[j]=temp
   return list_index


if __name__ == "__main__":
    app.run()