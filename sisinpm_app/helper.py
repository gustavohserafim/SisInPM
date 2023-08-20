import requests
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


def get_access_token(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers).json()

    return r.get("access_token")
