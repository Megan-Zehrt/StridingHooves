#import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_user
# model the class after the user table from our database
from flask_app import DATABASE
import re
import base64

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Post:
   def __init__(self, data:dict):
      self.id = data['id']
      self.pole_amount = data['pole_amount']
      self.how_to_build = data['how_to_build']
      self.how_it_works = data['how_it_works']
      self.image = data['image']
      self.user_id = data['user_id']
      self.created_at = data['created_at']
      self.updated_at = data['updated_at']

      #Add additional columns from database here

   def info(self):
      returnStr = f"Pole amount = {self.pole_amount} || How to build = {self.how_to_build} || How it works = {self.how_it_works} image = {self.image}"
      return returnStr

#CREATE
   @classmethod
   def create_one(cls, data:dict):
      query = "INSERT INTO posts (pole_amount, how_to_build, how_it_works, image, user_id) VALUES (%(pole_amount)s, %(how_to_build)s, %(how_it_works)s, %(image)s, %(user_id)s)"
    #  print("this is the model file")
      result = connectToMySQL(DATABASE).query_db(query, data)
      return result
       
   # now we use the class methods to query our database 

#READ
   @classmethod
   def get_all(cls) -> list:
      query = "SELECT * FROM posts;"
      #make sure to call the connectToMySQL function with the schema you are targeting

      results = connectToMySQL(DATABASE).query_db(query)
      #create an empty list to append our instances of posts
      if not results:
         return []

      instance_list = []
      # iterate over the db results anad create instances of posts with cls.
      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list

   @classmethod
   def get_one(cls, data):
      query = "SELECT * FROM posts WHERE posts.id = %(id)s;"
    #  print(query)
      results = connectToMySQL(DATABASE).query_db(query, data)
      if not results:
         return []

      instance_list = []

      for dictionary in results:
         instance_list.append(cls(dictionary))
      return instance_list


   @classmethod
   def get_by_email(cls,data):
      query = "SELECT * FROM posts WHERE email = %(email)s;"
      result = connectToMySQL(DATABASE).query_db(query,data)
      # Didn't find a matching user
      if len(result) < 1:
         return False
      return cls(result[0])


# Validators

   @staticmethod
   def validator(data: dict) -> bool:
      is_valid = True

      if(len(data['pole_amount'])) ==0:
         flash("How many poles does this exercise take?", "err_posts_pole_amount")
         is_valid = False

      if(len(data['how_to_build']) < 1):
         flash("How do you build your exercise?", "err_posts_how_to_build")
         is_valid = False

      if(len(data['how_it_works']) < 1):
         flash("How does your exercise work?", "err_posts_how_it_works")
         is_valid = False


     # if(data['image']) ==0:
      #   flash("Please upload an image for your exercise", "err_posts_image")
       #  is_valid = False

      return is_valid
      #run through some if checks -> if if checks come out to be bad then is_valid = False



# SAVE
   @classmethod
   def save(cls,data):
      query = "INSERT INTO posts (pole_amount, how_to_build, how_it_works, image) VALUES (%(pole_amount)s, %(how_to_build)s, %(how_it_works)s, %(image)s);"
      result = connectToMySQL(DATABASE).query_db(query, data)
      return result

   #DELETE
   @classmethod
   def delete(cls, data):
      query = "DELETE FROM posts WHERE id = %(id)s;"
      return connectToMySQL(DATABASE).query_db(query, data)

   #UPDATE
   @classmethod
   def update(cls, data):
      query = "UPDATE posts SET pole_amount = %(pole_amount)s, how_to_build = %(how_to_build)s, how_it_works = %(how_it_works)s, image = %(image)s WHERE id = %(id)s;"
      return connectToMySQL(DATABASE).query_db(query, data)

# for the show route to show the one post that you selected on the "view post" URL
   @classmethod
   def get_one_post(cls, data):
      query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id WHERE posts.id = %(id)s;"
     # print(query)
      results = connectToMySQL(DATABASE).query_db(query, data)
      if results:

         one_post = cls(results[0])
         for dictionary in results:

            users_data = {
               **dictionary,
               "id": dictionary["users.id"],
               "updated_at": dictionary["users.updated_at"],
               "created_at": dictionary["users.created_at"]
            }
        #    print(users_data)

            u = model_user.User(users_data)
            one_post.u = u
         return one_post

# for the display route where it shows the user that created the post in the "posted by" coloumn
   @classmethod
   def get_posts(cls):
      query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id;"
      results = connectToMySQL(DATABASE).query_db(query)
      instance_list = []
      if results:
         for dictionary in results:
        #    print("*****************",dictionary['first_name'])
            one_post = cls(dictionary)

            users_data = {
               **dictionary,
               "id": dictionary["users.id"],
               "updated_at": dictionary["users.updated_at"],
               "created_at": dictionary["users.created_at"]
            }
      #      print(users_data)

            u = model_user.User(users_data)
            one_post.u = u
            instance_list.append(one_post)
         return instance_list
      return []

# converting Image to Base64

   @staticmethod
   def image_to_base64(image_path):
      #with open(image_path, "r") as image_file:
       #  encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
      encoded_string = base64.b64encode(image_path.read())
      return encoded_string

# base64_string = image_to_base64("image.jpg")
