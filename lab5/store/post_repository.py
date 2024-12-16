from loguru import logger
from sqlalchemy import select

from schemas import PostSchema, PostAddSchema

from .models import PostORM
from .database import session_maker


class PostRepository:
    """
    Repository for Post ORM model.

    Methods:
        add_one(cls, post: PostAddSchema) -> PostSchema: Add a post to the database.
        add_many(cls, posts: list[PostAddSchema]) -> list[PostSchema]: Add multiple posts to the database.
        find_all(cls, skip: int = 0, limit: int = 100) -> list[PostSchema]: Find all posts in the database.
        find_one(cls, post_id: int) -> PostSchema | None: Find a post in the database by id.
        update_one(cls, post: PostSchema) -> PostSchema | None: Update a post in the database by id.
        delete_one(cls, post_id: int) -> bool: Delete a post in the database by id.
    """

    @classmethod
    @logger.catch
    async def add_one(cls, post: PostAddSchema) -> PostSchema:
        """
        Add a post to the database.

        Args:
            post (PostAddSchema): The post to add.

        Returns:
            PostSchema: The added post.
        """
        logger.info(f"Adding post: {post}.")
        post_orm = PostORM(**post.model_dump())
        async with session_maker() as session:
            session.add(post_orm)
            await session.flush()
            await session.commit()
        return PostSchema.model_validate(post_orm)

    @classmethod
    @logger.catch
    async def add_many(cls, posts: list[PostAddSchema]) -> list[PostSchema]:
        """
        Add multiple posts to the database.

        Args:
            posts (list[PostAddSchema]): The posts to add.

        Returns:
            list[PostSchema]: The added posts.
        """
        logger.info(f"Adding {len(posts)} posts.")
        posts_orm = [PostORM(**post.model_dump()) for post in posts]
        async with session_maker() as session:
            session.add_all(posts_orm)
            await session.flush()
            await session.commit()
        return [PostSchema.model_validate(post_orm) for post_orm in posts_orm]

    @classmethod
    @logger.catch
    async def find_all(cls, skip: int = 0, limit: int = -1) -> list[PostSchema]:
        """
        Find all posts in the database.

        Args:
            skip (int, optional): The number of posts to skip. Defaults to 0.
            limit (int, optional): The maximum number of posts to return. Defaults to -1 (all posts).

        Returns:
            list[PostSchema]: The found posts.
        """
        if limit == -1 and skip == 0:
            logger.info(f"Finding all posts.")
            query = select(PostORM)
        elif limit == -1:
            logger.info(f"Finding all posts from {skip}.")
            query = select(PostORM).offset(skip)
        elif skip == 0:
            logger.info(f"Finding all posts with a limit of {limit}.")
            query = select(PostORM).limit(limit)
        else:
            logger.info(f"Finding all posts from {skip} to {limit}.")
            query = select(PostORM).offset(skip).limit(limit)
        async with session_maker() as session:
            post_orms = (await session.execute(query)).scalars().all()
        return [PostSchema.model_validate(post_orm) for post_orm in post_orms]

    @classmethod
    @logger.catch
    async def find_one(cls, post_id: int) -> PostSchema | None:
        """
        Find a post in the database by id.

        Args:
            post_id (int): The id of the post to find.

        Returns:
            PostSchema: The found post.
        """
        logger.info(f"Finding post with id: {post_id}.")
        async with session_maker() as session:
            post_orm = await session.get(PostORM, post_id)

        if post_orm is None:
            return None
        return PostSchema.model_validate(post_orm)

    @classmethod
    @logger.catch
    async def update_one(cls, post: PostSchema) -> PostSchema | None:
        """
        Update a post in the database by id.

        Args:
            post (PostSchema): The post with updated fields.

        Returns:
            PostSchema: The updated post.
        """
        logger.info(f"Updating post with id: {post.id}.")
        async with session_maker() as session:
            post_orm = await session.get(PostORM, post.id)
            if post_orm is None:
                logger.info(f"Post with id: {post.id} not found.")
                return None

            post_orm.user_id = post.user_id
            post_orm.title = post.title
            post_orm.body = post.body
            await session.flush()
            await session.commit()

        logger.success(f"Post with id: {post.id} updated.")
        return PostSchema.model_validate(post_orm)

    @classmethod
    @logger.catch
    async def delete_one(cls, post_id: int) -> bool:
        """
        Delete a post in the database by id.

        Args:
            post_id (int): The id of the post to delete.

        Returns:
            bool: True if the post was deleted, False otherwise.
        """
        logger.info(f"Deleting post with id: {post_id}.")
        async with session_maker() as session:
            post_orm = await session.get(PostORM, post_id)
            if post_orm is None:
                logger.info(f"Post with id: {post_id} not found.")
                return False

            await session.delete(post_orm)
            await session.flush()
            await session.commit()

        logger.success(f"Post with id: {post_id} deleted.")
        return True
