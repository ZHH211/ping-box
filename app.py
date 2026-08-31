"""盯几个网址，挂了记一笔，有 webhook 就推出去。"""
from flask import Flask, jsonify, request, session, send_from_directory

import config
import db
import ping

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = config.SECRET_KEY

db.init_db()


def logged_in():
    return session.get("ok") is True


@app.get("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/login")
def login():
    body = request.get_json(silent=True) or {}
    if str(body.get("password", "")) != config.ADMIN_PASSWORD:
        return jsonify({"ok": False, "msg": "密码不对"}), 400
    session["ok"] = True
    return jsonify({"ok": True})


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


@app.get("/api/me")
def me():
    return jsonify({"ok": logged_in(), "webhook": bool(config.WEBHOOK_URL)})


@app.get("/api/targets")
def targets():
    if not logged_in():
        return jsonify({"ok": False}), 401
    return jsonify({"ok": True, "items": db.list_targets(), "logs": db.recent_logs()})


@app.post("/api/targets")
def create_target():
    if not logged_in():
        return jsonify({"ok": False}), 401
    body = request.get_json(silent=True) or {}
    name = str(body.get("name", "")).strip()
    url = str(body.get("url", "")).strip()
    if not name or not url:
        return jsonify({"ok": False, "msg": "名字和网址都要填"}), 400
    if not url.startswith("http://") and not url.startswith("https://"):
        return jsonify({"ok": False, "msg": "网址要以 http 开头"}), 400
    new_id = db.add_target(name, url)
    return jsonify({"ok": True, "id": new_id})


@app.delete("/api/targets/<int:target_id>")
def remove_target(target_id):
    if not logged_in():
        return jsonify({"ok": False}), 401
    db.delete_target(target_id)
    return jsonify({"ok": True})


@app.post("/api/check")
def check():
    if not logged_in():
        return jsonify({"ok": False}), 401
    items = db.list_targets()
    bad = []
    for t in items:
        ok, status, ms, err = ping.ping_url(t["url"])
        msg = err or ("HTTP " + str(status))
        db.add_log(t["id"], ok, status, ms, msg)
        if not ok:
            bad.append("%s %s (%s)" % (t["name"], t["url"], msg))
    note = ""
    if bad:
        note = ping.notify("有地址打不通：\n" + "\n".join(bad))
    elif not items:
        note = "还没加网址"
    else:
        note = "都通"
    return jsonify({"ok": True, "bad": len(bad), "note": note, "logs": db.recent_logs()})


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True)
