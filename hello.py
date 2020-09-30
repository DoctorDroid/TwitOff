from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/new_page')
def new_page():
    return 'You found the second page!'

""" **Shell comands to deploy app locally
set FLASK_APP=hello.py
flask run
"""
'''
if you add this, you can run the flask app as :
Python hello.py
'''
if __name__ == '__main__':
    app.run(debug=True)