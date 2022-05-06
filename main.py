from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask('app')
app.config['SECRET_KEY'] = 'qEChL7R3SpF72cEA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    created_at = db.Column(db.String())
    update_at = db.Column(db.String())

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    image = db.Column(db.String())
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.String())
    update_at = db.Column(db.String())

@app.route('/')
def index():
  if 'user_id' not in session:
    return redirect('/login')
  contacts = Contacts.query.filter_by(user_id=session['user_id']).all()
  return render_template('index.html', contacts=contacts)

# depois do login
@app.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    new_contacts = Contacts(
        name = name,
        email = email,
        phone = phone,
        user_id = session['user_id']
    )
    db.session.add(new_contacts)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    delete = Contacts.query.filter_by(id=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    update = Contacts.query.filter_by(id=id).first()
    update.name = name
    update.email = email
    update.phone = phone
    db.session.commit()
    return redirect('/')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register')
def register():
  return render_template('register.html')
  
@app.route('/signup', methods=['POST'])
def up():
  name_input = request.form.get('name')
  email_input = request.form.get('email')
  password_input = request.form.get('password')

  # Verificar se já existe o email no bd
  user = Users.query.filter_by(email=email_input).first()
  if user:
    return redirect('/register')

  new_user = Users(
    name=name_input,
    email=email_input,
    password=generate_password_hash(password_input))
  db.session.add(new_user)
  db.session.commit()
  return redirect('/login')

@app.route('/signin', methods=['POST'])
def signup():
  email_input = request.form.get('email')
  password_input = request.form.get('password')

  # Verificar se já existe o email no bd
  user = Users.query.filter_by(email=email_input).first()
  if not user:
    return redirect('/login')

  if not check_password_hash(user.password, password_input):
    return redirect('/login')

  # Guardar usuário na sessão
  session['user_id'] = user.id
  return redirect('/')
  
if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080)