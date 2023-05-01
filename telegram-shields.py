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
        "logoSvg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240"><defs><linearGradient gradientUnits="userSpaceOnUse" y2="51.9" y1="11.536" x2="28.836" x1="46.136" id="a"><stop offset="0" stop-color="#37aee2"/><stop offset="1" stop-color="#1e96c8"/></linearGradient></defs><g transform="scale(3.4682)"><circle fill="url(#a)" r="34.6" cx="34.6" cy="34.6"/><path fill="#fff" d="M14.4 34.3l23.3-9.6c2.3-1 10.1-4.2 10.1-4.2s3.6-1.4 3.3 2c-.1 1.4-.9 6.3-1.7 11.6l-2.5 15.7s-.2 2.3-1.9 2.7c-1.7.4-4.5-1.4-5-1.8-.4-.3-7.5-4.8-10.1-7-.7-.6-1.5-1.8.1-3.2 3.6-3.3 7.9-7.4 10.5-10 1.2-1.2 2.4-4-2.6-.6l-14.1 9.5s-1.6 1-4.6.1c-3-.9-6.5-2.1-6.5-2.1s-2.4-1.5 1.7-3.1z"/></g></svg>""",
        "message": f"{members} members",
        "schemaVersion": 1
    }

    return shields_schema


if __name__ == "__main__":
    script_path = os.path.dirname(__file__)
    config_path = os.path.join(script_path, "config.toml")
    config = toml.load(config_path)

    app.run(debug=False, port=config["quart_port"])
