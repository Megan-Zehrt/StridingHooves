from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for, jsonify
from flask_app.models.model_user import User
from flask_app.models.model_post import Post
from flask_bcrypt import Bcrypt
import base64        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument




@app.route("/exercise")
def exercise():
  if not "user_id" in session:
    return redirect('/signup')
 # print(session['user_id'])

  posts = Post.get_posts()
  user = User.get_one({ 'id': session['user_id']})
  return render_template("exercise.html", posts = posts, user=user)

@app.route("/design")
def design():
  if not "user_id" in session:
    return redirect('/signup')
 # print(session['user_id'])

  posts = Post.get_posts()
  user = User.get_one({ 'id': session['user_id']})
  return render_template("design.html", posts = posts, user=user)

@app.route("/dashboard")
def dashboard():
  if not "user_id" in session:
    return redirect('/signup')
 # print(session['user_id'])

  posts = Post.get_posts()
  user = User.get_one({ 'id': session['user_id']})
  return render_template("dashboard.html", posts = posts, user=user)

@app.route('/logout')
def logout():
  session.pop('user_id')
  return redirect("/")


# Login Session
@app.route("/login", methods=['POST'])
def login_process():
   if request.method == "POST":
      session['email'] = request.form['email']
      session['password'] = request.form['password']
      if not User.validator_login(request.form):
        return redirect ('/signup')

      # see if the username provided exists in the database
      data = { "email" : request.form["email"] }
      user_in_db = User.get_by_email(data)
      # user is not registered in the db
      if not user_in_db:
          flash("Invalid Email", "err_users_loginemail")
          return redirect("/signup")
      if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
          flash("Invalid Password", "err_users_loginpassword")
          return redirect('/signup')
      # if the passwords matched, we set the user_id into session
      session['user_id'] = user_in_db.id
      return redirect('/dashboard')

  # Main Page
@app.route("/signup")
def signup():
  if "user_id" in session:
    return redirect('/dashboard')
  return render_template("Home.html")

# Register Session
@app.route('/register', methods=['POST'])
def submit_form():

        is_valid = User.validator(request.form)

        if not is_valid:
            return redirect('/signup')

        pw_hash = bcrypt.generate_password_hash(request.form['password'])
       # print(pw_hash)
        # put the pw_hash into the data dictionary
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password" : pw_hash
        }

        if request.method == 'POST':
          session['first_name'] = request.form['first_name']
          session['last_name'] = request.form.get('last_name')
          session['email'] = request.form.get('email')
          # Call the save @classmethod on User
        user_id = User.save(data)
        # store user id into session
        session['user_id'] = user_id
        return redirect('/dashboard')





