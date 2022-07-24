from uuid import uuid4
from api.v1.models.post_model import Post
from shared.utils.datetime_util import utc_now
from api import db


class PostService:
    def get_by_id(self, id):
        return Post.query.filter_by(id=id).first()

    def get_list(self, page, item_per_page):
        return Post.query.order_by(Post.created_at.desc()).paginate(page, item_per_page)

    def add(self, post_data: dict):
        post = Post()
        post.id = str(uuid4())
        post.title = post_data.get("title")
        post.description = post_data.get("description")
        post.created_by = post_data.get("created_by")

        db.session.add(post)
        db.session.commit()
        return self.get_by_id(post.id)

    def update(self, post, data_update: dict):
        post.title = data_update.get("title")
        post.description = data_update.get("description")
        post.updated_at = utc_now()
        db.session.commit()
        return True

    def delete(self, post):
        if post is not None:
            db.session.delete(post)
            db.session.commit()
        else:
            raise ValueError("Not found this post")
        return True
