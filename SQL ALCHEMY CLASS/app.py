from flask import Flask, render_template # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import desc # type: ignore

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
db=SQLAlchemy(app)


class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(40))



class Post(db.Model):
    id=db.Column(db.Integer, primary_key = True) 
    title=db.Column(db.String(200)) 
    content = db.Column(db.Text)
    user_id= db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable = False
    )

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/add")
def add():
    admin = user(name = "harshu", role = "admin")
    db.session.add(admin)
    db.session.commit()

    return "<p>Data Added</p>"




@app.route("/show")
def show():
   users = user.query.all()  # Fixed: lowercase 'user' and 'users'
   output = ""
   for usr in users:  # Fixed: lowercase 'usr'
       print(usr.name)  # Fixed: correct variable name and proper indentation
       output += f"<p>{usr.name} - {usr.role}</p>"  # Optional: build output to display

   return output if output else "<p>No users found</p>"




@app.route("/delete/<name>")
def delete(name):
    user_to_delete = user.query.filter_by(name=name).first()
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return f"<p>User '{name}' deleted successfully</p>"
    else:
        return f"<p>User '{name}' not found</p>"
    
@app.route("/show_all")
def show_all():
   student = user.query.order_by(desc(user.id)).all()
   
   return render_template('index.html', student = student)



@app.route("/show_user")
def show_user():
    all_users = user.query.filter(user.name.like("A%")).all()

    return render_template("index.html", student = all_users)


# @app.route("/post")
# def post():
#     user = User(name = "alice", email = "alice@xyz.com", role = 1)
#     db.session.add(user)
#     db.session.commit()
#     post = Post(title = "New post", 
#                 content = "here is breaking news",
#                 user_id = user.id)
    
#     db.session.add(user)
#     db.session.commit()

#     return f"{post.title}, {post.user_id}"







@app.route("/post")
def post():
    new_user = user(name = "Alice", email = 'alice@xy.com', role = "24")
    db.session.add(new_user)
    db.session.commit()
    post = Post(title = "News post",
                content = "here is breaking news",
                user_id = new_user.id)

    db.session.add(post)
    db.session.commit()

    return f"{post.title}, {post.user_id}"


@app.route("/post_by/<name>")
def post_by(name):
    new_user = user.query.filter_by(name = name).first()

    if new_user:
        post = Post(title = "User post",
                content = f"this post created by {new_user.name}",
                user_id = new_user.id)
        db.session.add(post)
        db.session.commit()
        return f"{post.title}, {post.content}"
    
    return "no user found"
    



@app.route('/show_post')              
def show_post():
    # Join user and Post tables correctly
    results = db.session.query(user, Post)\
        .join(Post, user.id == Post.user_id)\
        .all()

    # Print for debugging
    for u, p in results:
        print(f"{p.title} by {u.name}")

    return render_template("post.html", posts=results)
    


@app.route('/submit')
def submit():
    pass



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Store registered users
users = []

@app.route('/')
def home():
    return "<h1>Hello Test</h1>"

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Store user in users list
        user = {
            'name': name,
            'email': email,
            'password': password
        }
        users.append(user)

        # PRG Pattern: Redirect to success page after POST
        return redirect(url_for('registration_success', name=name, email=email))

    return render_template("registration.html")

@app.route('/registration/success')
def registration_success():
    # Get data from URL parameters (after redirect)
    name = request.args.get('name')
    email = request.args.get('email')
    return render_template("success.html", name=name, email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['name'] = user['name']
                session['email'] = user['email']
                # PRG Pattern: Redirect to profile after login
                return redirect(url_for('profile'))

        return "Invalid email or password!"

    return render_template("login.html")

@app.route('/profile')
def profile():
    if 'name' in session:
        return f"<h1>Profile</h1><p>Name: {session['name']}</p><p>Email: {session['email']}</p>"
    return "<h1>No user logged in</h1>"

@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('email', None)
    return "Logged out successfully!"

if __name__ == '__main__':
    app.run(debug=True)

