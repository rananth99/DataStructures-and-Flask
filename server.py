from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import linked_list
import hash_table
import binary_search_tree
import queue
import stack
import random

# app
app = Flask(__name__)

# -------------------------------
# SQLALCHEMY CONFIGURATIONS
# -------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# configure sqlite3 to enforce foreign key contraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


db = SQLAlchemy(app)
now = datetime.now()

# -------------------------------
#           MODELS
# -------------------------------

# User Table : this contains all the columns related to user and relationship with other table
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")

# BlogPost Table : this contains all the columns related to blogpost and relationship with other table
class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# -------------------------------
#           ROUTES
# -------------------------------

# 1) this route is for creating new users
@app.route("/user", methods=["POST"])
def create_user():
    # takes in the data sent as part of the request body and populates the User table
    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"],
    )
    # this adds the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200

# 2) this route is to get all the user details in the descending order 
@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    # this retrieves all the records from the User table in ascending order by default
    users = User.query.all()
    # creating an object of LinkedList to access all the linked list methods
    all_users_ll = linked_list.LinkedList()
    # traversing through each of the user from all the users retrieved from the database
    for user in users:
        # calling the user defined function to insert the records at the beginning of the linked list
        all_users_ll.insert_at_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    return jsonify(all_users_ll.to_list()), 200

# 3) this route is to get all the user details in the ascending order
@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    # this retrieves all the records from the User table in ascending order by default
    users = User.query.all()
    # creating an object of LinkedList to access all the linked list methods
    all_users_ll = linked_list.LinkedList()
    # traversing through each of the user from all the users retrieved from the database
    for user in users:
        # calling the user defined function to insert the records at the end of the linked list
        all_users_ll.insert_at_end(
            {
                "id":user.id,
                "name":user.name,
                "email":user.email,
                "address":user.address,
                "phone":user.phone
            }
        )

    return jsonify(all_users_ll.to_list()), 200

# 4) this route is to fetch a particular user details given the user id 
@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    # this retrieves all the records from the User table in ascending order by default
    users = User.query.all()
    # creating an object of LinkedList to access all the linked list methods
    all_users_ll = linked_list.LinkedList()
    # traversing through each of the user from all the users retrieved from the database
    for user in users:
        # calling the user defined function to insert the records at the beginning of the linked list
        all_users_ll.insert_at_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
    # calling the user defined function to  retrieve a particular user details given the user id
    user = all_users_ll.get_user_by_id(user_id)

    return jsonify(user), 200
    
# 5) this route is to delete a particular user from the database given the user id
@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # this queries the User table and filters it based on the user id given as a parameter in the route
    user = User.query.filter_by(id=user_id).first()
    # this deletes that particular user from the database and commits the changes
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message":"user deleted"}), 200

# 6) this route is for creating new blog posts
@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    # takes in the data sent as part of the request body and populates the BlogPost table
    data = request.get_json()
    # this fetches the first user with the given user id
    user = User.query.filter_by(id=user_id).first()
    # this is to check if that particular user exists or not
    if not user:
        return jsonify({"message":"user does not exist"}), 400
    else:
        # creating an object of HashTable to access all the methods belonging to hash table
        ht = hash_table.HashTable(10)
        # creating key-value pairs for all the data belonging to the blog post
        ht.add_key_value("title", data["title"])
        ht.add_key_value("body", data["body"])
        ht.add_key_value("date", now)
        ht.add_key_value("user_id", user_id)

        # this is getting the data ready for adding to the database
        new_blog_post = BlogPost(
            title = ht.get_value("title"),
            body = ht.get_value("body"),
            date = ht.get_value("date"),
            user_id = ht.get_value("user_id")     
        )
        # this adds the new blog post to the database
        db.session.add(new_blog_post)
        db.session.commit()

        return jsonify({"message":"blog post created"}), 200

# 7) this route is for searching for a particular blog post  
@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    # this retrieves all the blog posts from the BlogPost table in ascending order by default
    blog_posts = BlogPost.query.all()
    # performing a shuffle over the retrieved data so that it is not in any particular order
    random.shuffle(blog_posts)
    
    # creating an object of BinarySearchTree to access all the methods belonging to the binary search tree 
    bst = binary_search_tree.BinarySearchTree()
    # traversing through each of the post
    for post in blog_posts:
        # calling the user defined insert function of BinarySearchTree to insert the data
        bst.insert(
            {
                "id" : post.id,
                "title" : post.title,
                "body" : post.body,
                "user_id" : post.user_id
            }
        )
    # calling the user defined search function of BinarySearchTree to search for a particular blog post
    post = bst.search(blog_post_id)
    print(post)
    if not post:
        return jsonify({"message":"post not found"}), 400
    else:
        return jsonify(post), 200

# 8) this route is for converting the large body content of blog post to a numerical equivalent
@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    # this retrieves all the blog posts from the BlogPost table in ascending order by default
    blog_posts = BlogPost.query.all()
    # creating an object of Queue to access all the method belonging to queue
    q = queue.Queue()
    # traversing through each post
    for post in blog_posts:
        # calling the user defined enqueue function of Queue to insert each post into the queue
        q.enqueue(post)
    
    return_list = []
    # traversing through all the blog posts
    for _ in range(len(blog_posts)):
        # calling the user defined dequeue function of Queue to remove each post from the queue
        post = q.dequeue()
        numeric_body = 0
        # traversing through each character of the body of the post
        for char in post.data.body:
            # summing the ascii value of each character of the post
            numeric_body += ord(char)
        # storing the numeric value as body of the post
        post.data.body = numeric_body

        return_list.append(
            {
                "id":post.data.id,
                "title":post.data.title,
                "body":post.data.body,
                "user_id":post.data.user_id
            }
        )
    return jsonify(return_list), 200

# 9) this route is for deleting blog posts
@app.route("/blog_post/<blog_count>", methods=["DELETE"])
def delete_blog_post(blog_count):
    # this retrieves all the blog posts from the BlogPost table in ascending order by default
    blog_post = BlogPost.query.all()
    # taking the number of posts to be deleted from the route as a parameter
    count = int(blog_count)
    # creating an object of Stack to access all the methods belonging to stack
    st = stack.Stack()
    # traversing through each of the post
    for post in blog_post:
        # calling the user defined push function of Stack to insert the post into the stack
        st.push(post)
    # checking if the number of posts to be deleted is less than the total number of posts present
    if count < len(blog_post):
        # traversing through the count
        for _ in range(count):
            # calling the user defined pop function of Stack to delete the post from the stack
            post_to_delete = st.pop()
            # deleting the contents of the post from the database and commiting the changes
            db.session.delete(post_to_delete.data)
            db.session.commit()
        return jsonify({"message":"deleted successfully"}), 200
    else:
        return jsonify({"message":"count out of bound"}), 400


if __name__ == '__main__':
    app.run(debug=True)







