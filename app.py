from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import init_db, add_link, get_links, delete_link
from config import user,passw
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize the database
init_db()

# Home route
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    links = get_links(search_query)
    return render_template('index.html', links=links, search_query=search_query)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check for superuser credentials
        if username == 'admin' and password == 847726:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# Admin route to add and delete links
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'add_link' in request.form:
            category = request.form['category']
            link = request.form['link']
            if category and link:
                add_link(category, link)
                return redirect(url_for('admin'))
        elif 'delete_link' in request.form:
            link_id = request.form['link_id']
            delete_link(link_id)
            return redirect(url_for('admin'))
    
    links = get_links()
    return render_template('admin.html', links=links)

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
