import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename
from glooba.backend.config import Config
from glooba.backend.extensions import db, migrate, login_manager
from glooba.backend.models.user import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads/profile_pics')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'login'

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
                flash('All fields are required.')
                return redirect(url_for('signup_email'))
            dummy_email = f'{username}@glooba.com'
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=dummy_email).first():
                flash('Username or email already exists.')
                return redirect(url_for('signup_email'))
            new_user = User(full_name=full_name, username=username, email=dummy_email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('profile_setup'))
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('splash')) # Redirect to home if already logged in
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            user = User.query.filter_by(username=username).first()
            # Also check if they entered an email
            if not user:
                user = User.query.filter_by(email=username).first()

            if user is None or not user.check_password(password):
                flash('Invalid username or password')
                return redirect(url_for('login'))

            login_user(user, remember=remember)
            return redirect(url_for('splash')) # Redirect to a real homepage later
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('welcome'))

    @app.route('/profile/setup', methods=['GET', 'POST'])
    @login_required
    def profile_setup():
        if request.method == 'POST':
            bio = request.form.get('bio')
            interests = request.form.getlist('interests')
            current_user.bio = bio
            current_user.interests = ",".join(interests) if interests else ""
            if 'profile_pic' in request.files:
                file = request.files['profile_pic']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    unique_filename = f"{current_user.id}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                    current_user.profile_pic = f'uploads/profile_pics/{unique_filename}'
            db.session.commit()
            return redirect(url_for('personalization'))
        return render_template('profile_setup.html')

    @app.route('/personalization')
    @login_required
    def personalization():
        return render_template('personalization.html')

    return app
