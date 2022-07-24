from datetime import timezone
from uuid import uuid4

from api import bcrypt, db
from flask import current_app
from shared.constants import UUID_V4_LENGTH
from shared.utils.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.String(UUID_V4_LENGTH), primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    hash_password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    role = db.Column(db.String(10), nullable=False, default="user")
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<User email={self.email}, role={self.role}>"

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.hash_password = hash_bytes.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash_password, password)
