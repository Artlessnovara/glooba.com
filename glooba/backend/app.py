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
    app.config['PROFILE_PIC_UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads/profile_pics')
    app.config['POST_MEDIA_UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads/posts')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'login'

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
            # ... (signup logic)
            return redirect(url_for('profile_setup'))
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # ... (login logic)
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('welcome'))

    @app.route('/profile/setup', methods=['GET', 'POST'])
    @login_required
    def profile_setup():
        if request.method == 'POST':
            # ... (profile setup logic)
            return redirect(url_for('personalization'))
        return render_template('profile_setup.html')

    @app.route('/personalization')
    @login_required
    def personalization():
        return render_template('personalization.html')

    @app.route('/composer', methods=['GET', 'POST'])
    @login_required
    def composer():
        if request.method == 'POST':
            content = request.form.get('content')
            media_file = request.files.get('media')
            media_type = None
            media_url = None
            if media_file and media_file.filename != '':
                filename = secure_filename(media_file.filename)
                upload_path = os.path.join(app.config['POST_MEDIA_UPLOAD_FOLDER'], filename)
                media_file.save(upload_path)
                media_url = f'uploads/posts/{filename}'
                if 'image' in media_file.mimetype:
                    media_type = 'image'
                elif 'video' in media_file.mimetype:
                    media_type = 'video'
            if content or media_url:
                new_post = Post(content=content, media_type=media_type, media_url=media_url, user_id=current_user.id)
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('home'))
            flash("You need to add content or media to post.")
            return redirect(url_for('composer'))
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
        return {"count": post.likes_count, "active": not not like}

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
        return {"count": post.comments_count}

    @app.route('/glow_post/<int:post_id>', methods=['POST'])
    @login_required
    def glow_post(post_id):
        post = Post.query.get_or_404(post_id)
        post.glows_count += 1
        db.session.commit()
        return {"count": post.glows_count}

    @app.route('/share_post/<int:post_id>', methods=['POST'])
    @login_required
    def share_post(post_id):
        post = Post.query.get_or_404(post_id)
        post.shares_count += 1
        db.session.commit()
        return {"count": post.shares_count}

    @app.cli.command("create-dummy-data")
    def create_dummy_data():
        """Creates dummy users, stories, and posts for testing."""
        # ... (dummy data logic)
        print("Dummy data created.")

    return app
