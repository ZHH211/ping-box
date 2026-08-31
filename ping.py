"""探一下网址通不通。挂了就往 webhook 推一条。"""
import time

import httpx

import config


def ping_url(url):
    t0 = time.time()
    try:
        with httpx.Client(follow_redirects=True, timeout=config.TIMEOUT) as client:
            resp = client.get(url)
        ms = int((time.time() - t0) * 1000)
        ok = 200 <= resp.status_code < 400
        return ok, resp.status_code, ms, ""
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return False, None, ms, str(e)[:180]


def notify(text):
    if not config.WEBHOOK_URL:
        return "没配 webhook，只记了日志"
    payload = {"msgtype": "text", "text": {"content": text}}
    try:
        with httpx.Client(timeout=8) as client:
            r = client.post(config.WEBHOOK_URL, json=payload)
        if r.status_code >= 400:
            return "webhook 没推出去：" + str(r.status_code)
        return "已推 webhook"
    except Exception as e:
        return "webhook 失败：" + str(e)[:120]
