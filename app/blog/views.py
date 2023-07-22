from flask import render_template, request
from sqlalchemy import select, func, desc
from app.database import engine, posts

from . import blog


POSTS_PER_PAGE = 10


@blog.route("/", methods=["GET"])
def get_posts():
    # get/validate pagination if exists
    ppage = None
    if request.args.get("page"):
        try:
            ppage = int(request.args.get("page")) - 1
            if ppage < 0:
                return render_template("404.html"), 404
        except ValueError:
            return render_template("404.html"), 404

    with engine.connect() as connection:
        query = select(posts).limit(POSTS_PER_PAGE).order_by(desc(posts.c.created_at))
        if ppage:
            query = query.offset(POSTS_PER_PAGE * ppage)
        results = connection.execute(query).all()
        if not results:
            return render_template("404.html"), 404

        # pagination
        qry = select(func.count()).select_from(posts)  # TODO: where(posts.c.public=True)
        row_count = connection.execute(qry).scalar()
        pages = row_count // POSTS_PER_PAGE
        if row_count % POSTS_PER_PAGE > 0:
            pages += 1
        return render_template(
            "blog/index.html",
            total=row_count,
            posts=results,
            pages=[i for i in range(1, pages + 1)],
        )


@blog.route("/post/<int:id>", methods=["GET"])
def post_detail(id):
    try:
        post_id = int(id)
        if post_id < 0:
            return render_template("404.html"), 404

        with engine.connect() as connection:
            post_query = select(posts).where(posts.c.id == post_id)
            post_result = connection.execute(post_query).first()
            return render_template("blog/post.html", post=post_result)

    except ValueError:
        return render_template("404.html"), 404
