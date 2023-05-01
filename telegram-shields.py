#!/usr/bin/env python3

import os
import toml
from quart import Quart, request
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ServerTimeoutError
import json

app = Quart("Quart APIs")


@app.before_serving
async def init_session():
    app.session = ClientSession()


@app.route("/tgmembercount")
async def shields():
    chat_id = request.args.get("chat_id", None)
    if not chat_id: return "Example: tgmembercount?chat_id=pythontelegrambotgroup"
    if not chat_id.startswith("@"):
        chat_id = f"@{chat_id}"

    url = f"https://api.telegram.org/bot{config['telegram_api_key']}/getChatMembersCount?chat_id={chat_id}"

    try:
        async with app.session.get(url, timeout=ClientTimeout(total=10)) as r:
            _json = json.loads(await r.text())
    except ServerTimeoutError:
        return 500, "Timeout reached."

    if _json["ok"] == False:
        return 400, "Invalid chat_id."

    print(_json)

    members = _json["result"]

    shields_schema = {
        "color": "1d93d2",
        "label": "Telegram",
        "namedLogo": "telegram",
        "logoColor": "blue",
        "message": f"{members} members",
        "schemaVersion": 1
    }

    return shields_schema


if __name__ == "__main__":
    script_path = os.path.dirname(__file__)
    config_path = os.path.join(script_path, "config.toml")
    config = toml.load(config_path)

    app.run(debug=False, port=config["quart_port"])
