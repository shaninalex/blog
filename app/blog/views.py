from sqlalchemy import insert
from app.database import engine, posts

from . import blog


@blog.route("/create", methods=['GET'])
def get_posts():
    with engine.connect() as connection:
        ins = insert(posts).values(
            title="test 123",
            body="test body"
        )
        result = connection.execute(ins)
        connection.commit()
        print(result.inserted_primary_key)
        return "posts", 200

# @blog_bp.route("/all", methods=['GET'])
# def get_posts_all():
#     with engine.connect() as connection:
#         sel = select(posts)
#         res = connection.execute(sel)
#         print(res.fetchall())
#         return "posts", 200
