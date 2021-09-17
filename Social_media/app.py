from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
import re 


app = Flask(__name__)
app.secret_key = 'Harsh@1526'
mysql=MySQL()
#mysql_config....................................................................................................................................
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='iconnect'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)
#................................................................................................................................................


@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('prof.html', username=session['username'], name=session['name'],sno=session['id'])
    else:
       return render_template('index.html')

@app.route("/login/", methods=['GET','POST'])
def login():
    msg=""
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)

    #output if something goes wrong
    

    msg='101 failed'
    if 'loggedin' in session:
        return render_template('prof.html', username=session['username'], name=session['name'],sno=session['id'])
    
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
         # Create variables for easy access
         username = request.form['username']
         password = request.form['password']
         # Check if account exists using MySQL
         cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
         # Fetch one record and return result
         account = cursor.fetchone()
   
         # If account exists in accounts table in out database
         if account:
            # Create session data, we can access this data in other routes
             print("exist")
             session['loggedin'] = True
             session['id'] = account['id']
             session['username'] = account['username']
             session['name']=account['name']
             # Redirect to home page
             #return 'Logged in successfully!'
             return redirect(url_for('prof'))
         else:
             # Account doesnt exist or username/password incorrect
             msg = '101 Incorrect username/password!'
             return render_template('index.html',msg=msg)
    else:
        msg=""
       
    return render_template('index.html',msg=msg)  
         
     
@app.route("/signup/", methods=['GET','POST'])
def signup():
    msg=""
    #signup queries
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    
    #output if something goes wrong
    msg='202 failed'
        #check if the session isn't present already
    if 'loggedin' in session:
         # User is loggedin show them the home page
         print("in session")
         return render_template('prof.html', username=session['username'], name=session['name'],sno=session['id'])
    else:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'username' in request.form and 'password' in request.form and 'rep-password' in request.form and 'gender' in request.form:
             name=request.form['name']
             email=request.form['email']
             username = request.form['username']
             password = request.form['password']
             rep_password=request.form['rep-password']
             gender=request.form['gender']
             if(password==rep_password):
                 cursor.execute('SELECT * FROM users WHERE username = %s', (username))
                 account = cursor.fetchone()
                 if account:
                     print ("exist")
                     msg="202 user already exist!"
                     return render_template('index.html',msg=msg)
                 elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                     msg = '202 Invalid email address!'
                 elif not re.match(r'[A-Za-z0-9]+', username):
                     msg = '202 Username must contain only characters and numbers!'
                 elif not username or not password or not email:
                     msg = '202 Please fill out the form!'
                 else:
                     cursor.execute('INSERT INTO users (name, email, password,gender, username) VALUES (%s,%s,%s,%s,%s)', (name, email, password, gender,username))
                     conn.commit()
                     cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                     account = cursor.fetchone()
                     print("registered")
                     session['loggedin'] = True
                     session['id'] = account['id']
                     session['username'] = account['username']
                     session['name']=account['name']
                     session['email']=account['email']
                     session['gender'] = account['gender']
                     # Redirect to home page
                     #return 'Logged in successfully!'
                     return redirect(url_for('prof'))
             else:
                 msg="202 Password Mismatch"
        else:
            msg="202 Enter some data"
    return render_template("index.html",msg=msg)           
    

     



@app.route('/profile/')
def prof():
    # Check if user is loggedin
    if 'loggedin' in session:
   
        # User is loggedin show them the home page
        return render_template('prof.html', username=session['username'], name=session['name'],sno=session['id'])
    # User is not loggedin redirect to login page
    return redirect(url_for('home')) 

@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('home'))

    
if __name__ == "__main__":
    app.run(debug=True)