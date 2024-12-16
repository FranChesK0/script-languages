from sqlalchemy.orm import Mapped, mapped_column

from .database import Model


class PostORM(Model):
    """
    ORM model that represents a Post.

    Attributes:
        id (int): The id of the post.
        user_id (int): The id of the user who created the post.
        title (str): The title of the post.
        body (str): The body of the post.
    """

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int]
    title: Mapped[str]
    body: Mapped[str]
