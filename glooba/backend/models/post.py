from datetime import datetime, timezone
from glooba.backend.extensions import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    glows_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Post {self.id}>'
