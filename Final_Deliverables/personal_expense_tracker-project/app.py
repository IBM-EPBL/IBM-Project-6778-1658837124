from flask import Flask, render_template, redirect,url_for,request, flash
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, DateField
from wtforms.validators import DataRequired,InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wtforms import StringField, DecimalField, SubmitField, DateField
import ibm_db,ibm_db_dbi,sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mail import Mail, Message
from sendgrid.helpers.mail import From, To
import smtplib
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content



SUBJECT = "Budget"
s = smtplib.SMTP('smtp.gmail.com', 587)
def sendgridmail(user,TEXT):
    sg = sendgrid.SendGridAPIClient('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')
    from_email = Email("shaamatechnology@gmail.com") # add the team senders mail id 
    to_email = To(user)
    subject = "Budget Exceeded"
    content = Content("text/plain",TEXT)
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
    



ibm_db_conn = ibm_db.connect('''DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cgz83208;PWD=K56N6PSUzD5ZcQ3f''','','')


connection = ibm_db_dbi.Connection(ibm_db_conn)
cursor = connection.cursor()
# connection = sqlite3.connect('database/db.sqlite', check_same_thread=False)
# cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expense (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	title VARCHAR(50) NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	amount FLOAT NOT NULL, 
	date DATE , 
	PRIMARY KEY (id)
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS user (
	id INTEGER NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	password VARCHAR(100), 
	name VARCHAR(1000), 
    budget FLOAT, 
    number VARCHAR(10),
    gender VARCHAR(100),
    address VARCHAR(100),
	PRIMARY KEY (id), 
	UNIQUE (email)
)''')

connection.commit()
cursor.execute("SELECT * from user where id = 0")
lu = cursor.fetchone()
if not lu:
    cursor.execute('''INSERT INTO user VALUES (0,'admin@admin','admin','admin',0,null,null,null);''')
    cursor.execute('''INSERT INTO expense VALUES (0,0,'null','null',0,'1000-01-01')''')
    connection.commit()

class User(UserMixin):
    def __init__(self, id, email, password, name,active=True):
         self.id = id
         self.email = email
         self.password = password
         self.name = name
         self.authenticated = False
         self.active = active
    def is_active(self):
         return self.active
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id

class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),InputRequired()])
    category = StringField('Category', validators=[DataRequired(),InputRequired()])
    amount = DecimalField('Amount', validators=[DataRequired(),InputRequired()])
    date = DateField('Date')
    submit = SubmitField('Submit')

    def __repr__(self):
        return f"ExpenseForm('{self.title}', '{self.category}', {self.amount}, {self.date})"



app = Flask(__name__)



app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app.config['SECRET_KEY'] = 'top-secret!'
# app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'apikey'
# app.config['MAIL_PASSWORD'] = os.environ.get('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')
# app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('shaamatechnology@gmail.com')
# mail = Mail(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

    

@login_manager.user_loader
def load_user(user_id):
   
   cursor.execute("SELECT * from user where id = (?)",(user_id,))
   lu = cursor.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2], lu[3]) 


    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    cursor.execute("SELECT * from user WHERE email = ?",(email,))
    user=cursor.fetchone()
    print()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if user==None or not check_password_hash(user[2], password):
         flash('Please check your login details and try again.')
         return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    LUser = load_user(user[:][0])
    # if the above check passes, then we know the user has the right credentials
    login_user(LUser, remember=remember)
    return redirect(url_for('home'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])    
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    
     # if this returns a user, then the email already exists in database
    cursor.execute("SELECT * from user WHERE email = ?",(email,))
    if cursor.fetchone():
        flash('Email address already exists')
        return redirect(url_for('signup'))
    
    #creating user id
    cursor.execute('''SELECT id FROM user ORDER BY id DESC;''')
    user_id=cursor.fetchone()[0]+1
    print('registered user id === ',user_id)


    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    print(user_id,email,generate_password_hash(password, method='sha256'),name,0)
    cursor.execute('INSERT INTO user VALUES (?,?,?,?,?,null,null,null);', (user_id,email,generate_password_hash(password, method='sha256'),name,0,))
    connection.commit()
    cursor.execute("SELECT * from user WHERE email = ?",(email,))
    user=cursor.fetchone()
    print()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if user==None or not check_password_hash(user[2], password):
         flash('Please check your login details and try again.')
         return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page
    LUser = load_user(user[:][0])
    # if the above check passes, then we know the user has the right credentials
    login_user(LUser, remember=False)
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/index',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        number = request.form.get('number')
        gender = request.form.get('gender')
        address = request.form.get('address')
        cursor.execute('UPDATE user SET number=?,gender=?,address=? WHERE email=?;', (number, gender, address, current_user.email,))
        connection.commit()
        return redirect(url_for('index'))
        
    if current_user.is_authenticated:
        cursor.execute("SELECT * from user WHERE email = ?",(current_user.email,))
        details=list(cursor.fetchone())
        print('detail',details)
        if details[5]==None:
            details[5]='Not Updated'
        if details[6]==None:
            details[6]='Not Updated'
        if details[7]==None:
            details[7]='Not Updated'
        return render_template('index.html',details=details)
    
    return render_template('index.html')

# assign home route and / route to home 
@app.route('/',methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        budget = request.form.get('budget')
        print(budget)
        cursor.execute('UPDATE user SET budget=? WHERE email=?;', (budget, current_user.email,))
        connection.commit()
        return redirect('/')
    if current_user.is_authenticated:
        cursor.execute("SELECT id,budget from user WHERE email = ?",(current_user.email,))
        k=cursor.fetchone()
        print(k)
        user_id=k[0]
        totalBudgetNow=k[1]
        
        d=datetime.datetime.now()
        print(d.strftime("%m"),d.strftime("%Y"))
        current_month=d.strftime("%B")
        
        cursor.execute("SELECT SUM(amount) from expense WHERE user_id = ? AND MONTH(date) = ? AND YEAR(date) = ?",(user_id,d.strftime("%m"),d.strftime("%Y"),))
        k=cursor.fetchone()[0]
        totalExpenseNow=0
        if k!=None:
            totalExpenseNow=k
            
        cursor.execute("SELECT COUNT(*),SUM(amount) from expense WHERE user_id = ?",(user_id,))
        k=cursor.fetchone()
        print('k======',k)
        totalItems=0
        totalExpense=0
        if k!=None:
            if k[0]!=None:
                totalItems=k[0]
            if k[-1]!=None:
                totalExpense=k[-1]
        
        if totalBudgetNow<totalExpenseNow and totalBudgetNow!=0:
            try:
                sendgridmail(current_user.email,"You have Exceeded Your budget")
            finally:
                cursor.execute('UPDATE user SET budget=? WHERE email=?;', (totalExpenseNow, current_user.email,))
                print('budget updated')
                totalBudgetNow=totalExpenseNow
                connection.commit()
                
                    
        return render_template('home.html', email=current_user.email ,name=current_user.name,totalExpense=totalExpense,totalItems=totalItems,totalExpenseNow=totalExpenseNow,totalBudgetNow=totalBudgetNow,current_month=current_month)

    return render_template('home.html')

@app.route('/view')
def view():
    if current_user.is_authenticated:
        cursor.execute("SELECT id from user WHERE email = ?",(current_user.email,))
        k=cursor.fetchone()
        print(k)
        user_id=k[0]
        cursor.execute("SELECT * from expense WHERE user_id = ?",(user_id,))
        all_expenses =cursor.fetchall()
        print(all_expenses)
        
        return render_template('view.html', expenses=all_expenses,email=current_user.email ,name=current_user.name)

    
    return render_template('view.html')

@app.route('/add', methods=['POST', 'GET'])
@login_required
def add():
  form = ExpenseForm()
  #if form successfully validated
  if form.validate_on_submit():

  # we create an expense object
    cursor.execute("SELECT id from user WHERE email = ?",(current_user.email,))
    user_id=cursor.fetchone()[0]
    
    #creating expense id
    cursor.execute('''SELECT id FROM expense ORDER BY id DESC;''')
    expense_id=cursor.fetchone()[0]+1
    print('created expense id === ',expense_id)
    
    cursor.execute('INSERT INTO expense VALUES (?,?,?,?,?,?);', (expense_id, user_id, form.title.data, form.category.data, str(form.amount.data), form.date.data,))
    connection.commit()
    return redirect(url_for('home'))

  form.date.data = datetime.datetime.now()
  return render_template('add.html', form=form)
  
@app.route("/update/<int:expense_id>", methods=['GET', 'POST'])
@login_required
def update(expense_id):
    cursor.execute("SELECT id from user WHERE email = ?",(current_user.email,))
    user_id=cursor.fetchone()[0]
    cursor.execute("SELECT * from expense WHERE (user_id = ? AND id = ?)",(user_id,expense_id,))
    expense=cursor.fetchone()
    form = ExpenseForm()
    print('updating expense_id=======',expense_id)
        # if the form is validated and submited, update the data of the item
        # with the data from the field
    if form.validate_on_submit():
        
        cursor.execute('UPDATE expense SET title=?,category=?,amount=?,date=? WHERE id=?;', (form.title.data, form.category.data, str(form.amount.data), form.date.data, expense_id,))
        connection.commit()
        return redirect(url_for('view'))
        # populate the field with data of the chosen expense 
    elif request.method == 'GET':
        form.title.data = expense[2]
        form.category.data = expense[3]
        form.amount.data = expense[4]
        form.date.data = expense[5]
    return render_template('add.html', form=form, title='Edit Expense')

@app.route("/delete/<int:expense_id>")
@login_required
def delete(expense_id):
    print('deleting expense_id=======',expense_id)
    cursor.execute("DELETE FROM expense WHERE id=?;",(expense_id,))
    connection.commit() 
    
    return redirect(url_for('view'))

if __name__ == '__main__':
     app.run(debug=True,host='0.0.0.0',port=8080,threaded=True)