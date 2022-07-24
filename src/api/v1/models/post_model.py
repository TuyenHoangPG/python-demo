from datetime import timezone

from api import db
from api.v1.dtos.user_dto import UserDto
from shared.constants import UUID_V4_LENGTH
from shared.utils.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)
from sqlalchemy.ext.hybrid import hybrid_property


class Post(db.Model):
    __tablename__ = "Posts"

    id = db.Column(db.String(UUID_V4_LENGTH), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now)
    created_by = db.Column(
        db.String(UUID_V4_LENGTH), db.ForeignKey("Users.id"), nullable=False
    )
    __author = db.relationship(
        "User", backref=db.backref("post", lazy="joined"), lazy=True
    )

    def __repr__(self) -> str:
        return (
            f"<Posts id={self.id}, title={self.title}, author={self.author.first_name}>"
        )

    @hybrid_property
    def updated_at_str(self):
        updated_at_utc = make_tzaware(
            self.updated_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(updated_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @property
    def author(self):
        return UserDto(
            id=self.__author.id,
            email=self.__author.email,
            first_name=self.__author.first_name,
            last_name=self.__author.last_name,
        ).to_dict()
