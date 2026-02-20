from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

# Database initialization
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE NOT NULL, 
                  password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER NOT NULL, 
                  title TEXT NOT NULL, 
                  content TEXT NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html', page='home', username=session['username'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!')
            return redirect(url_for('register'))
    
    return render_template('index.html', page='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT id, username FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    
    return render_template('index.html', page='login')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)', 
                  (session['user_id'], title, content))
        conn.commit()
        conn.close()
        flash('Post created successfully!')
        return redirect(url_for('view_posts'))
    
    return render_template('index.html', page='create_post')

@app.route('/posts')
def view_posts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, title, content FROM posts WHERE user_id = ?', (session['user_id'],))
    posts = c.fetchall()
    conn.close()
    
    return render_template('index.html', page='view_posts', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)

