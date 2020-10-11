from flask import Flask, render_template, request
from .db_model import DB, User
from .twitter import add_user_tweepy, update_all_users
from .predict import predict_user
from os import getenv

def create_app():
    '''Create and configure an instance of our Flask application'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)  # Connect Flask app to SQLAlchemy DB

    @app.route('/')
    def root():
        return render_template('base.html', title='TwitOff - Home', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def add_or_update_user(name=None, message=''):
        name = name or request.values['user_name']

        try:
            if request.method == "POST":
                add_user_tweepy(name)
                message = f"User {name} successfully added!"
            else:
                message = f"User {name} not found on Twitter."
            tweets = User.query.filter(User.username == name).one().tweet
        except Exception as e:
            print(f'Error adding {name}: {e}')
            tweets = []

        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = 'Try again with two different twitter users.'
        else:
            prediction = predict_user(user1, user2, tweet_text)

            message = f'''{tweet_text} was more likely to have been tweeted by {user1 if prediction else user2} 
                          than {user2 if prediction else user1}'''

        return render_template('predict.html', title='Prediction Results', message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title = 'Database has been reset!!', users=User.query.all())
        
    @app.route('/update') #methods=GET is default
    def update():
        update_all_users()
        return render_template('base.html', title = 'All tweets have been updated!', users=User.query.all())
    return app