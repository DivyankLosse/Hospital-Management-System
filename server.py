from flask import Flask, request, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from controller import signup_new_user, check_user
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize OAuth
oauth = OAuth(app)

oauth.register(
    "google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    "facebook",
    client_id=os.getenv("FACEBOOK_CLIENT_ID"),
    client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
    authorize_url="https://www.facebook.com/dialog/oauth",
    access_token_url="https://graph.facebook.com/oauth/access_token",
    client_kwargs={"scope": "email"},
)

oauth.register(
    "apple",
    client_id=os.getenv("APPLE_CLIENT_ID"),
    client_secret=os.getenv("APPLE_CLIENT_SECRET"),
    authorize_url="https://appleid.apple.com/auth/authorize",
    access_token_url="https://appleid.apple.com/auth/token",
    client_kwargs={"scope": "email name"},
)

@app.route("/login/<provider>")
def login(provider):
    if provider not in ["google", "facebook", "apple"]:
        return "Invalid provider", 400
    return oauth.create_client(provider).authorize_redirect(url_for("authorize", provider=provider, _external=True))

@app.route("/authorize/<provider>")
def authorize(provider):
    client = oauth.create_client(provider)
    token = client.authorize_access_token()
    user_info = client.parse_id_token(token) if provider == "google" else token.get("userinfo", {})
    
    email = user_info.get("email")
    name = user_info.get("name", "")
    
    if not check_user(email, ""):  # Check if user exists (password not needed for OAuth)
        signup_new_user(email, "", None, None)  # Register with empty password
    
    session["user"] = {"email": email, "name": name}
    return redirect(url_for("main_redirect"))

@app.route("/main")
def main_redirect():
    return "Login successful! Please return to the application."

if __name__ == "__main__":
    app.run(debug=True)