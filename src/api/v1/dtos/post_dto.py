class PostDto:
    def __init__(self, id, title, description, updated_at, author):
        self.id = id
        self.title = title
        self.description = description
        self.updated_at = updated_at
        self.author = author

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "updated_at": self.updated_at,
            "author": self.author,
        }
