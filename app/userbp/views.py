"""
Based on [Create a Flask Application With Google Login](https://realpython.com/flask-google-login/#creating-a-google-client) article
"""
import requests
import json
from . import userbp, GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from flask import current_app, redirect, request, url_for
from app.userbp.user import User
from flask_login import (
    login_required,
    login_user,
    logout_user,
)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@userbp.route("/user/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = current_app.config["client"].prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@userbp.route("/user/login/callback")
def callback():
    code = request.args.get("code")
    client = current_app.config["client"]
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        userinfo = userinfo_response.json()
        users_email = userinfo["email"]
        picture = userinfo["picture"]
        users_name = userinfo["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User(name=users_name, email=users_email, profile_pic=picture)

    # Doesn't exist? Add it to the database.
    if not User.get(users_email):
        User.create(users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("blog.get_posts"))


@userbp.route("/user/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("blog.get_posts"))
