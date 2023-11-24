from flask import Flask, render_template, request, session, redirect, url_for, flash
from resources.aws import aws
from resources.azure import azure
from resources.gcp import gcp
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session,sessionmaker
import os
app = Flask(__name__)
app.secret_key = 'RGV2T3BzIERhc2hib2FyZAo='

app.register_blueprint(aws)
app.register_blueprint(azure)
app.register_blueprint(gcp)
app.config['SECRET_KEY'] = 'dev_env'
DB_URL = os.getenv('DB_URL')
engine=create_engine(f"{DB_URL}")
db=scoped_session(sessionmaker(bind=engine))



@app.route('/home')
@app.route('/')
def home():
    return render_template ('others/index.html')

########################## REGISTER FORM ####################################
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=="POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm=request.form.get('confirm')
        password_hash = generate_password_hash(password)
        select = "SELECT email FROM account WHERE email=:email"
        emaildata = db.execute(text(select), {"email":email}).fetchone()
        if emaildata==None:

                if password==confirm:
                    put = "INSERT INTO account(username,email,password) VALUES(:username,:email,:password)"
                    db.execute(text(put),
                    {"username":username, "email":email, "password":password_hash})
                    db.commit()
         
                    return redirect(url_for('login'))
                else:
                    flash("password does not match","danger")
                    return render_template('others/Register.html')
        else:
            flash("user already existed, please login or contact admin","danger")
            return render_template('others/Register.html')
    
    return render_template('others/Register.html')

########################## LOGIN FORM #################################
@app.route('/login', methods=['GET','POST'])
def login():
    global email
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(password)
        #env set
        session['user_email'] = email
        print(session['user_email'])
        
        selectuser = "SELECT email FROM account WHERE email=:email"
        emaildata = db.execute(text(selectuser), {"email":email}).fetchone()
        selectpassword = "SELECT password FROM account WHERE email=:email"
        passworddata = db.execute(text(selectpassword), {"email":email}).fetchone()
        print(emaildata)
        print(passworddata)
        if emaildata is None:
            flash("No username. Can you register now? ","danger")
            return render_template('others/LogIn.html')
        else:
            # for passwor_data in passworddata:
                if check_password_hash(passworddata[0],password):                    
                    # flash("You are now logged in!!","success")
                    return redirect(url_for('providers')) #to be edited from here do redict to either svm or home
                else:
                    flash("incorrect password","danger")
                    return render_template('others/LogIn.html')
    
    return render_template('others/LogIn.html')

#################################### PROVIDER PAGE ##########################
@app.route('/providers')
def providers():
    return render_template('others/Providers.html')

################## SERVICE PAGE ###################
@app.route('/service')
def service():
    return render_template('others/Service.html')

################## ABOUTUS PAGE #################
@app.route('/about')
def about():
    return render_template('others/About.html')

################## CONTACT PAGE #################
@app.route('/contact')
def contact():
    return render_template('others/Contact.html')

if __name__ == "__main__":
    app.run(debug='True')
