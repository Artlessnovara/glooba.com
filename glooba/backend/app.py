from flask import Flask, render_template, request, redirect, url_for
from glooba.backend.config import Config
from glooba.backend.extensions import db, migrate
from glooba.backend.models.user import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure tables are created with the app context
    # This is a workaround for the difficult environment.
    with app.app_context():
        db.create_all()

    @app.route('/')
    def splash():
        return render_template('splash.html')

    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')

    @app.route('/signup')
    def signup():
        return render_template('signup_options.html')

    @app.route('/signup/email', methods=['GET', 'POST'])
    def signup_email():
        if request.method == 'POST':
            full_name = request.form.get('fullname')
            username = request.form.get('username')
            password = request.form.get('password')

            if not full_name or not username or not password:
                return redirect(url_for('signup_email'))

            dummy_email = f'{username}@glooba.com'
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=dummy_email).first():
                return redirect(url_for('signup_email'))

            new_user = User(full_name=full_name, username=username, email=dummy_email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('profile_setup'))

        return render_template('signup.html')

    @app.route('/profile/setup', methods=['GET', 'POST'])
    def profile_setup():
        return render_template('profile_setup.html')

    return app
