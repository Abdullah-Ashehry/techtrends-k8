import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('app.log')  # Log to file
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()  # Log to console (stdout)
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Function to get a database connection.
# This function connects to database with the name `database.db`
db_connection_counter = 0 
def get_db_connection():
    global db_connection_counter  # Declare the global variable
    db_connection_counter += 1  # Increment the connection counter
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    app.logger.debug('retuning DB connection')
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    app.logger.debug('getting post id', post_id)
    return post


# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    app.logger.debug('getting all the posts')
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.debug('no posts available')
        return render_template('404.html'), 404
    else:
        app.logger.debug('returning post')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            app.logger.debug('No title provided')
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.debug('record inserted')

            return redirect(url_for('index'))
    app.logger.debug('returning create.html')
    
    return render_template('create.html')

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Status request successfull')
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    total_posts = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]  # Get total number of posts
    connection.close()
    
    response = app.response_class(
        response=json.dumps({
            "status": "success",
            "code": 0,
            "data": {
                "TotalPosts": total_posts,
                "TotalConnections": db_connection_counter  # Return total number of database connections
            }
        }),
        status=200,
        mimetype='application/json'
    )
    app.logger.debug('Metrics request successful')
    return response

# start the application on port 3111
if __name__ == "__main__":
    ## stream logs to a file
    # logging.basicConfig(filename='app.log', level=logging.DEBUG, force=True)
    
    app.run(host='0.0.0.0', port='3111')