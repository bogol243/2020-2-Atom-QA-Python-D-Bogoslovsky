from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "user1": "111",
    "user2": "222"
}


@auth.verify_password
def verify_password(username, password):
    
    if username in users and users[username] == password:
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

@app.route('/logout')
@auth.login_required
def logout():
    return f"{auth.current_user()} was logout!", 401


@app.route('/posts')
def posts():
    return 'posts'


@app.route('/comments')
def comments():
    return 'comments'

@app.route('/albums')
def albums():
    return 'albums'

@app.route('/photos')
def photos():
    return 'photos'

@app.route('/todos')
def todos():
    return 'todos'


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5555)