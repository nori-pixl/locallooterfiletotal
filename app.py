import os, random
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# クラウド環境では固定の表示にする（エラー回避）
DISPLAY_IP = "192.168.0.1" # 表示用のダミーIP
DISPLAY_PORT = random.randint(1024, 65535)

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Share</title>
    <style>
        body { font-family: sans-serif; padding: 20px; text-align: center; background: #f0f4f8; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .url-box { background: #eee; padding: 10px; border-radius: 5px; font-weight: bold; color: #d63384; word-break: break-all; margin-bottom: 20px; }
        input[type="file"] { margin-bottom: 20px; }
        button { background: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 8px; width: 100%; font-size: 16px; }
        ul { list-style: none; padding: 0; text-align: left; }
        li { background: #fff; margin: 5px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📁 ファイル共有</h2>
        <p>共有用URL（イメージ）:</p>
        <div class="url-box">https://{{ ip }}:{{ port }}</div>
        
        <form method="post" enctype="multipart/form-data" action="/upload">
            <input type="file" name="file"><br>
            <button type="submit">アップロード</button>
        </form>
        <hr>
        <h3>共有済みファイル</h3>
        <ul>
            {% for f in files %}
            <li><a href="/download/{{ f }}" download>{{ f }}</a></li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # ファイルリストを取得
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, files=files, ip=DISPLAY_IP, port=DISPLAY_PORT)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '<script>alert("完了！"); window.location.href="/";</script>'

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    # Renderのポート設定
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
