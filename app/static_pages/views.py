from flask import render_template
from . import static_pages


# @static_pages.route("404", methods=["GET"])
# def page_404():
#     return render_template("404.html"), 404


# @static_pages.route("500", methods=["GET"])
# def page_500():
#     return render_template("500.html"), 500


@static_pages.route("/about", methods=["GET"])
def about():
    return render_template("static_pages/about.html"), 200