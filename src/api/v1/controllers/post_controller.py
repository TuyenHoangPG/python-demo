from api.v1.dtos.user_dto import UserDto
from api.v1.services.post_service import PostService
from api.v1.dtos.post_dto import PostDto
from api.v1.utils.notification_util import send_notification
from rq import Queue
from worker import redis_conn


class PostController:
    post_service = PostService()
    queue = Queue(connection=redis_conn)

    def view_detail(self, id):
        post = self.post_service.get_by_id(id)
        post_dto = PostDto(
            id=post.id,
            title=post.title,
            description=post.description,
            updated_at=post.updated_at_str,
            author=post.author,
        )

        return post_dto.to_dict()

    def get_list(self, page=0, item_per_page=5):
        data = self.post_service.get_list(page, item_per_page)
        total = data.total
        items = data.items
        items = [
            PostDto(
                id=post.id,
                title=post.title,
                description=post.description,
                updated_at=post.updated_at_str,
                author=post.author,
            ).to_dict()
            for post in items
        ]

        return total, items

    def add(self, data: dict):
        post = self.post_service.add(data)
        post_dto = PostDto(
            id=post.id,
            title=post.title,
            description=post.description,
            updated_at=post.updated_at_str,
            author=post.author,
        )

        # no_user_received_noti = send_notification(post.created_by)
        # print(no_user_received_noti)

        job = self.queue.enqueue_call(
            func=send_notification, args=(post.created_by,), result_ttl=5000
        )

        return post_dto.to_dict()

    def update(self, user, data_update: dict):
        post = self.post_service.get_by_id(data_update.get("id"))
        if post is None:
            raise ValueError("Not found this post")

        if user.id != post.created_by:
            raise PermissionError("Not allow edit this post")

        return self.post_service.update(post, data_update)

    def delete(self, user, id: str):
        post = self.post_service.get_by_id(id)
        if post is None:
            raise ValueError("Not found this post")

        if user.id != post.created_by:
            raise PermissionError("Not allow delete this post")

        return self.post_service.delete(post)
