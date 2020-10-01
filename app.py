
from flask import Flask
from .db_model import DB, User, Tweet

def create_app():
    '''Create and configure an instance of our flask app'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitoff.db'
    #absolute path = 'sqlite:///C:\\Users\\Timothy Eakin\\PycharmProjects\\pythonProject\\TwitOff\\twitoff.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to Twitoff'

    @app.route('/<username>/<followers>')
    def add_user(username, followers):
        user = User(username=username, followers=followers)
        DB.session.add(user)
        DB.session.commit()

        return f'{username} has been added to the DB'

    @app.route('/tweet/<tweet>/<user_id>')
    def add_tweet(tweet, user_id):
        tweet = Tweet(tweet=tweet, user_id=user_id)
        DB.session.add(tweet)
        DB.session.commit()

        return f'New tweet has been added to the DB'

    return app