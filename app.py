from flask import Flask, render_template, request, flash, redirect, url_for
import codecs
from flask.json.tag import PassDict
from flask_mail import Mail,Message
from random import randint

from flask.templating import render_template_string
import pymongo

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)
app = Flask(__name__, template_folder='html')
app.config["SECRET_KEY"]="Dzscnsjkcv151465!#%&*(*^zufhsjdfh"
myclient = pymongo.MongoClient("mongodb+srv://ayush:ayush@cluster0.azo8z.mongodb.net/Project?retryWrites=true&w=majority")
mydb = myclient["Project"]
mycol = mydb["Project"] 
mail = Mail(app)
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='xyzasak@gmail.com'
app.config['MAIL_PASSWORD']='Amit@2020'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)


# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
        return render_template("index.html")

@app.route('/login',methods=['GET', 'POST'])

def login():
    if request.method=='GET':
        username = request.args.get("Username")
        if(username):
            return render_template("login.html", Username = username)
        else:
            return render_template("login.html")
    elif request.method=='POST':
        if 'username' in request.form:
            username = request.form['username']
            password = request.form['password']
            x = mycol.find_one({"username":username,"password":password})
            if x is None:
                flash("Wrong Credentials!")
                return render_template("login.html" )
            else:
                nickname = x["username"]
                return render_template("final.html", Data = nickname)


@app.route('/register',methods=['GET', 'POST'])

def register():
    if request.method=='GET':
        return render_template("Registration.html")
    elif request.method=='POST':
        if 'username' in request.form:
            username = request.form['username']
            password = request.form['password']
            nickname = request.form['nickname']
            email = request.form['email']
            if (len(password)==0):
                flash("Password cannot be Empty!")
                return render_template("Registration.html")
            else:
                data = {"username":username,"password":password,"nickname":nickname,"email":email}
                x = mycol.insert_one(data)
                if(x):
                    return render_template("securityquestion.html", Username = username)

@app.route('/forgotpassword',methods=['GET', 'POST'])

def forgotpassword():
    error = None 
    if request.method=='GET':
        return render_template("forgotpasswrod.html")
    elif request.method=='POST':
        if 'username' in request.form:
            username = request.form['username']
            x = mycol.find_one({"username":username})
            if x:
                msg = Message(subject='OTP',sender='rajat.maini2020@vitbhopal.ac.in',recipients=[x["email"]])
                msg.body=str(otp)
                mail.send(msg)
                return render_template("f1.html",Username = username)
            else:
                flash('Enter valid username')
                return render_template("forgotpasswrod.html")

@app.route('/f1',methods=['POST'])

def f1():
    if request.method=='POST':
        if 'otp' in request.form:
          uotp = request.form['otp']
          Username = request.form['username']
          if (otp==int(uotp)):
              return render_template("Enterpassword.html",Username = Username)
          else:
                flash('Wrong Answer!')
                return render_template("f1.html", Username = Username)
              
@app.route('/chngpassword',methods=['GET','POST'])

def chngpassword():
    if request.method=='POST':
        if 'username' in request.form:
            username = request.form['username']
            password = request.form['password']
            x = mycol.find_one({"username":username})
            if x:
                 oldValue = {"username":username}
                 newValue = {'$set' :{"password":password}}
                 y = mycol.update_one(oldValue,newValue)
                 if y:
                    return redirect(url_for('login', Username = username))
            else:
                return("Wrong Username!")

@app.route('/final',methods=['GET','POST'])

def final():
    if request.method=='POST':
        if 'username' in request.form:
            username = request.form['username']
            ans1 = request.form['ans1']
            ans2 = request.form['ans2']
            ans3 = request.form['ans3']
            oldValue = {"username":username}
            newValue = {'$set' :{"ans1":ans1,"ans2":ans2,"ans3":ans3}}
            x = mycol.update_one(oldValue, newValue)
            if(x):
                return render_template("final.html", Data = username)

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.debug = True
    app.run('localhost', 5000)
