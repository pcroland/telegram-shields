#!/usr/bin/env python3

import os
import toml
from quart import Quart, request
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ServerTimeoutError
import json

app = Quart("Custom Telegram membercount endpoint for shields.io")


@app.before_serving
async def init_session():
    app.session = ClientSession()


@app.route("/tgmembercount")
async def shields():
    prefix = request.args.get("prefix", "")
    suffix = request.args.get("suffix", "members")
    chat_id = request.args.get("chat_id", None)
    if not chat_id: return "Example: tgmembercount?chat_id=pythontelegrambotgroup", 400
    if not chat_id.startswith("@"): chat_id = f"@{chat_id}"

    url = f"https://api.telegram.org/bot{config['telegram_api_key']}/getChatMembersCount?chat_id={chat_id}"
    try:
        async with app.session.get(url, timeout=ClientTimeout(total=10)) as r:
            _json = json.loads(await r.text())
    except ServerTimeoutError:
        return "Telegram API seems to be down.", 500
    if not _json["ok"]: return "Invalid chat_id.", 400

    members_str = " ".join(s.strip() for s in [prefix, str(_json["result"]), suffix] if s not in [None, ""])
    shields_schema = {
        "color": "1d93d2",
        "label": "Telegram",
        "message": members_str,
        "namedLogo": "telegram",
        "schemaVersion": 1
    }
    return shields_schema


if __name__ == "__main__":
    script_path = os.path.dirname(__file__)
    config_path = os.path.join(script_path, "config.toml")
    config = toml.load(config_path)

    app.run(debug=False, port=config["quart_port"])
