from flask import Flask
from flask import Flask, render_template, json, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
db = SQLAlchemy(app)

#create the database model
class User(db.Model):
    __tablename__ = "user_table"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    active = db.Column(db.String(10), unique=True)

    def __init__(self, email, password, name, active):
        self.email = email
        self.password = password
        self.name = name
        self.active = active
    
    def __repr__(self):
        return '<E-mail %r>' %self.email, '<Password %r>' %self.password, '<Name %r>' %self.name, '<Active %r>' %self.Active 
    
#Set homepage to index.html
@app.route('/')
def main():
        return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
        return render_template('signin.html')

@app.route('/',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _active = request.form['inputactive']
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

# Save user to the database
@app.route('/prereg', methods=['POST'])
def prereg():
   email = None
   password = None
   name = None
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       name = request.form['name']
       #Check if that email does not already exist
       if not db.session.query(User).filter(User.email == email).count():
           reg = User(email)
           db.session.add(reg)
           db.session.commit()
           return render_template('succss.html')
   return render_template('signup.html')

    
if __name__ == "__main__":
    app.debug = True
    app.run()
