from config import Secrets
from database import DB
from database.accounts import *

import requests

from base64 import b64decode
from flask import Flask, render_template, request

app = Flask(__name__)
DB.connect()
if not DB.is_connected:
    raise RuntimeError("Database access denied")

print("Connected to Database")


@app.route("/<string:token>")
def index(token: str):
    data = b64decode(token).decode().split('/', 3)
    guild_id, user_id = int(data[0]), int(data[1])
    server_name = data[2]

    create_guild_account(guild_id)
    add_account(guild_id, user_id)

    return render_template(
        "index.html",
        server_name=server_name,
        site_key=Secrets.site_key, token=token
    )


@app.post("/<string:token>/verify")
def verify(token: str):
    data = b64decode(token).decode().split('/', 3)
    guild_id, user_id = int(data[0]), int(data[1])
    server_name = data[2]

    response = request.form['g-recaptcha-response']

    data = {
        "response": response, "secret": Secrets.site_secret_key
    }
    resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    result = resp.json()

    user_ip = request.remote_addr
    if resp.ok and result["success"]:
        if user_ip is None or len(user_ip) <= 2:
            return render_template(
                "verify.html", server_name=server_name,
                error="Verification Failed!, make sure that you are not using any VPN or proxies")

        if ip_exists(guild_id, user_ip):
            return render_template(
                "verify.html", server_name=server_name,
                error="Verification Failed!, ALT Accounts are not allowed"
            )

        update_ip(guild_id, user_id, request.remote_addr)
        print(get_account(guild_id, user_id))
        return render_template("verify.html", server_name=server_name, log="Verification Successful")
    else:
        return render_template("verify.html", server_name=server_name, error="Verification Failed")
