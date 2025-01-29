from flask import Flask, request, render_template, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)    # Database instance created

# Database Model
class User(db.Model):  
    #Class Variables
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)    

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/')
def home():
    if  "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

#Login
@app.route('/login', methods=['POST'])   
def login():
    #Get the form data  
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username = username).first()
    #Check if the user exists in the database
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    #otherwise, redirect to the home page
    else:
        flash("Invalid Credentials, Please try again.", "error.")
        return render_template('index.html')

#Register
@app.route('/register', methods=['POST'])    
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username = username).first()
    if user:
        flash("User already exists.", "error.")
        return redirect(url_for('home'))    
        # return render_template('index.html', error="User already exists.")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)    #Add the new user to the database
        db.session.commit()    #Commit the changes  
        session['username'] = username #create new session for user
        return redirect(url_for('dashboard'))  #redirect to the dashboard

#Dashboard
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html', username=session['username'])  
    return redirect(url_for('home'))    

#Logout
@app.route('/logout')   
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info.") 
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)