from pydantic import BaseModel, ConfigDict


class PostAddSchema(BaseModel):
    """
    Schema for adding a post.

    Attributes:
        user_id (int): The ID of the user who created the post.
        title (str): The title of the post.
        body (str): The content of the post.
    """

    user_id: int
    title: str
    body: str

    model_config = ConfigDict(from_attributes=True)


class PostSchema(PostAddSchema):
    """
    Schema for retrieving a post.

    Attributes:
        id (int): The ID of the post.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
