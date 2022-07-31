#!/usr/bin/python3

# standard library
import sqlite3 as sql

# python3 -m pip install flask
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# Main page
@app.route('/')
def home():
    return render_template('login.html', msg = "Welcome")

@app.route('/login')
def rendlogin():
    return render_template('login.html', msg = "Welcome")

@app.route('/login',methods = ['POST'])
def login():
    row = None
    try:
        email = request.form['email']         # user email
        password = request.form['password']     # user password
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            # Query
            cur.execute("SELECT * FROM user WHERE email = ? AND password = ?",(email,password))
            row = cur.fetchone()
            # Execute
            con.commit()
    except Exception as e:
        print(e)
    finally:
        if row == None:                
            return render_template('login.html', msg = "Invalid email or password. Please try again.")
        else:
            return render_template('SecretPage.html', msg = "You have successfully logged in.")

#check if email exists
def checkemail(email):
    row = None
    try:
        # Database connectivity
        with sql.connect("database.db") as con:
            cur = con.cursor()
            # Query
            cur.execute("SELECT * FROM user WHERE email = ?",(email,))
            row = cur.fetchone()
            # Execute
            con.commit()
    except Exception as e:
        print("Error: ",e)
    finally:
        if row == None:                
            return True
        else:
            return False
        
@app.route('/signup')
def rendsignup():
    return render_template('signup.html', msg = "Please fill below information for signup")
    
#Signup
@app.route('/signup',methods = ['POST'])
def signup():
    status = False
    try:
        fname = request.form['fname']         #first name
        lname = request.form['lname']         #last name
        email = request.form['email']         # email
        password = request.form['password']   #password
        cpassword = request.form['cpassword'] #confirm password
        if password == cpassword:
            if checkemail(email) == True:
                with sql.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO user (fname,lname, email, password) VALUES (?,?,?,?)",(fname,lname,email,password))
                    con.commit()
                msg = "Thanks for registering. Please proceed with login."
                status = True
            else:
                msg = "Email already exists."
        else:
            msg = "Password doesn't match. Please recheck."
    except:
        msg = "Ops! error in operation"

    finally:
        if status == True:
            return render_template("thankyou.html")
        else:
            return render_template("signup.html",msg = msg)    #render page with message


if __name__ == '__main__':
    try:
        # ensure the sqliteDB is created
        con = sql.connect('database.db')
        print("Database connectivity is OK")
        #con.execute('DROP TABLE user')
        con.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,fname TEXT, lname TEXT, email TEXT, password TEXT)')
        print("Table created successfully")
        con.close()
        # begin Flask Application 
        app.run(host="0.0.0.0", port=2224, debug = False)
    except:
        print("Error Running application")

