# ping-box

盯几个网址。点一下探通不通，挂了记日志。`.env` 里填了 webhook 就会往钉钉/飞书自定义机器人推一条。

```bash
copy .env.example .env
pip install -r requirements.txt
python app.py
```

或 `start.bat`，5062 端口，密码默认 123456。

钉钉机器人地址填 `WEBHOOK_URL`。不填也能用，只是不推人。

主要文件：`ping.py` 探网址和推消息，`app.py` 接口，`static/app.js` 页面。
