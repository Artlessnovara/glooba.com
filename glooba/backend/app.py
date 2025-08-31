import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, current_user, login_required
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
                return redirect(url_for('signup_email'))
            dummy_email = f'{username}@glooba.com'
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=dummy_email).first():
                return redirect(url_for('signup_email'))
            new_user = User(full_name=full_name, username=username, email=dummy_email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('profile_setup'))
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Login logic will be implemented in Phase 3
        return render_template('login.html')

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
            return redirect(url_for('splash'))
        return render_template('profile_setup.html')

    return app
