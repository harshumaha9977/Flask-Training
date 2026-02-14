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

