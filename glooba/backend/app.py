import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename
from glooba.backend.config import Config
from glooba.backend.extensions import db, migrate, login_manager
from glooba.backend.models.user import User
from glooba.backend.models.story import Story
from glooba.backend.models.post import Post
from glooba.backend.models.interaction import Like, Comment, Glow, Share

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

    # with app.app_context():
    #     db.create_all()

    @app.route('/')
    def splash():
        return render_template('splash.html')

    @app.route('/home')
    @login_required
    def home():
        stories = Story.query.order_by(Story.timestamp.desc()).all()
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        return render_template('home.html', stories=stories, posts=posts)

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
            return redirect(url_for('home'))
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

    @app.route('/composer')
    @login_required
    def composer():
        return render_template('composer.html')

    # --- API Routes for Interactions ---
    @app.route('/like_post/<int:post_id>', methods=['POST'])
    @login_required
    def like_post(post_id):
        post = Post.query.get_or_404(post_id)
        like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if like:
            db.session.delete(like)
            post.likes_count -= 1
        else:
            like = Like(user_id=current_user.id, post_id=post.id)
            db.session.add(like)
            post.likes_count += 1
        db.session.commit()
        return {"likes": post.likes_count, "liked": not not like}

    @app.route('/comment_on_post/<int:post_id>', methods=['POST'])
    @login_required
    def comment_on_post(post_id):
        post = Post.query.get_or_404(post_id)
        comment_text = request.form.get('comment')
        if comment_text:
            comment = Comment(content=comment_text, user_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            post.comments_count += 1
            db.session.commit()
        return redirect(url_for('home'))

    @app.route('/glow_post/<int:post_id>', methods=['POST'])
    @login_required
    def glow_post(post_id):
        post = Post.query.get_or_404(post_id)
        # For simplicity, we're just incrementing. A real app might have more complex logic.
        post.glows_count += 1
        db.session.commit()
        return {"glows": post.glows_count}

    @app.route('/share_post/<int:post_id>', methods=['POST'])
    @login_required
    def share_post(post_id):
        post = Post.query.get_or_404(post_id)
        post.shares_count += 1
        db.session.commit()
        return {"shares": post.shares_count}

    @app.cli.command("create-dummy-data")
    def create_dummy_data():
        """Creates dummy users, stories, and posts for testing."""
        db.session.remove()
        db.drop_all()
        db.create_all()

        user1 = User(full_name="Alice", username="alice", email="alice@glooba.com")
        user1.set_password("password")
        user2 = User(full_name="Bob", username="bob", email="bob@glooba.com")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()

        story1 = Story(image_url="https://via.placeholder.com/300x500", user_id=user1.id)
        story2 = Story(image_url="https://via.placeholder.com/300x500", user_id=user2.id)
        story3 = Story(image_url="https://via.placeholder.com/300x500", user_id=user1.id)
        db.session.add_all([story1, story2, story3])

        post1 = Post(content="This is the first post on GLOOBA! #firstpost", user_id=user1.id, likes_count=245, comments_count=78, glows_count=320, shares_count=12)
        post2 = Post(content="Having a great day exploring the new app.", user_id=user2.id, likes_count=102, comments_count=15, glows_count=99, shares_count=5)
        post3 = Post(content="What is everyone up to? @bob", user_id=user1.id, likes_count=500, comments_count=150, glows_count=1200, shares_count=50)
        db.session.add_all([post1, post2, post3])

        db.session.commit()
        print("Dummy data created.")

    return app
