from flask import Flask,request,jsonify
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app=Flask(__name__)
import pymongo




#Database....

#connect to  DataBase
ENV='dev'


if ENV =='dev':
    app.debug=True
    #psycopg2.connect(database="netscore",user="postgres",password="r@ms@i143",host="localhost")
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:r@ms@i143@localhost/netscore'
    #app.config['SQLALCHEMY_BINDS']={'two':'postgresql://postgres:r@ms@i143@localhost/NetTrucks'}
    
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']='postgres://yzdgkuettqacnj:59d2398cd919d2fd596b4d66f800f4e3fc729adf0267914df501aa9e2a64fef6@ec2-34-230-198-12.compute-1.amazonaws.com:5432/d5uq7hviqqldfe'
db= SQLAlchemy(app)
migrate=Migrate(app,db)

class Check(db.Model):
    __tablename__='Login_api'
    __table_args__ = {'extend_existing': True}
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(200))
    password=db.Column(db.String(200))

def login_user(username, password):
    data=Check.query.filter(Check.username==username)
    fill=Check.query.filter(Check.password==password)
    dc=[]
    op=[]
    for j in fill:
        check={}
        check['username']=j.username
        check['password']=j.password
        dc.append(check)
    for i in data:
        form={}
        form['username']=i.username
        form['password']=i.password
        op.append(form)
    if bool(op)==True and bool(dc)==True:
        return "suc"
    else:
        return "unsuc"

#defalut route
@app.route('/')


def signup():
    return render_template('sign.html')

@app.route('/snv/',methods=['GET','POST'])
def fun4():
   username=request.form['fir']
   password=request.form['pass']

   mid=Check.query.filter(Check.username==username)
   
   mi=[]
   for j in mid:
        check={}
        check['username']=j.username
        mi.append(check)

   
    
   if bool(mi)==True:
       ci="username Already Taken"
       return render_template('sign.html',cc='{}'.format(ci))
   else:
       ml="successfully Register"
       data=Check(username=username,password=password)
       db.session.add(data)
       db.session.commit()
       return render_template('sign.html')
       




@app.route('/sai/',methods=['GET','POST'])
def index():
    username=request.args.get("username")
    password=request.args.get("password")
    flag=login_user(username,password)
    if flag =="suc":
        return jsonify("succ")
    else:
        return jsonify("error")

    



#run the app

if __name__ == '__main__':
    app.debug=True
    app.run()