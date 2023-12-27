from flask_app import app
from flask import render_template,redirect,request,session,flash, url_for, jsonify
from flask_app.models.model_post import Post
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt
import base64        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument




@app.route("/post/new")
def new_post():
    if not "user_id" in session:
        return redirect('/signup')

    posts= Post.get_all()
    return render_template("new.html", posts=posts)

@app.route("/create_post", methods=['POST'])
def create_post():
    is_valid = Post.validator(request.form)
    if not is_valid:
        return redirect('/post/new')

    image_path = request.files.get("image_path")

    base64 = Post.image_to_base64(request.files['image'])
    base64str = str(base64)

    new_base64 = base64str[2: -1]
    combo_base64 = "data:image/jpeg;base64,"

    full_base64 = combo_base64 + new_base64
    print(full_base64)

    data = {
      'pole_amount': request.form['pole_amount'],
      'how_to_build': request.form['how_to_build'],
      'how_it_works': request.form['how_it_works'],
      'image': base64,
      'user_id': session['user_id']
    }
    id = Post.create_one(data)
    return redirect("/exercise")

# Inverting a file from an Image to Base64

@app.route("/image_to_base64", methods=["GET"])
def image_to_base64():
    # Get the image path from the query string
    # Check if the image path is valid
    if image_path:
        # Try to convert the image to base64
        try:
            base64_string = image_to_base64(image_path)
            # Return the base64 string as a JSON response
            return jsonify({"base64_string": base64_string})
        except Exception as e:
            # Return an error message if something goes wrong
            return jsonify({"error": str(e)})
    else:
        # Return a message if the image path is missing
        return jsonify({"message": "Please provide an image path"})




# Show post

@app.route("/post/<int:id>")
def post_show_id(id):
  #  print("*********",id,"**********")
    if not "user_id" in session:
      return redirect('/signup')

    post = Post.get_posts()
    posts = Post.get_one_post({ 'id': id})
    user = User.get_one({ 'id': session['user_id']})
    return render_template("Show_post.html", posts = posts, user = user, post=post )

# Delete post
@app.route("/post/delete/<int:post_id>")
def delete_post(post_id):
   data = {
      'id': post_id
   }
   Post.delete(data)
   return redirect("/exercise")

# Edit post

@app.route("/post/edit/<int:id>")
def edit_post(id):
  if not "user_id" in session:
    return redirect('/signup')

    is_valid = Post.validator(request.form)
    if not is_valid:
        return redirect('/post/edit')

  data = {"id" : id}
  posts = Post.get_one_post(data)
 # print(posts)
  user = User.get_one({ 'id': session['user_id']})
  return render_template("post_edit.html", posts = posts, user=user)


@app.route("/post/edit", methods=['POST'])
def update_post():
    is_valid = Post.validator(request.form)
    if not is_valid:
        return redirect(f"/post/edit/{request.form['id']}")
    data = {
      'id' : request.form['id'],
      'name': request.form['name'],
      'description': request.form['description'],
      'instructions': request.form['instructions'],
      'time': request.form['time'],
      'under': request.form['under'],
      'user_id': session['user_id']
    }
    Post.update(data)
    return redirect("/exercise")

# Entry Page

@app.route("/")
def entry():
  if "user_id" in session:
    return redirect('/exercise')
  return render_template("entry.html")