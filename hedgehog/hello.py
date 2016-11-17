from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    return 'Hello, admin!'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' %username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id
