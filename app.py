
from flask import Flask, render_template, request
from .db_model import DB, User, Tweet
from .twitter import add_user_tweepy


def create_app():
    '''
    Create and configure an instance of our flask app
    '''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitoff.sqlite3'
    #absolute path = 'sqlite:///C:\\Users\\Timothy Eakin\\PycharmProjects\\pythonProject\\TwitOff\\twitoff.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app) #for connecting the app to SQLAlchemy

    @app.route('/')
    def root():
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def add_or_update_user(name=None, message=''):
        name = name or request.values['user_name']

        try:
            if request.method == "POST":
                add_user_tweepy(name)
                message = f"User {name} successfully added!"
            tweets = User.query.filter(User.username == name).one().tweet
        except Exception as e:
            print(f'Error adding {name}: {e}')
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)

    return app