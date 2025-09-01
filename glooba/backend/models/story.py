from datetime import datetime, timezone
from glooba.backend.extensions import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('stories', lazy=True))

    def __repr__(self):
        return f'<Story {self.id}>'
