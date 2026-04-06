import os, random
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 表示用のランダムなポート番号を生成（見た目用）
DISPLAY_PORT = random.randint(1024, 65535)

# HTMLのデザイン（スマホで見やすく、ご希望のURL形式を表示）
HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud File Share</title>
    <style>
        body { font-family: sans-serif; padding: 20px; text-align: center; background: #f0f4f8; }
        .card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
        .url-display { background: #333; color: #00ff00; padding: 15px; border-radius: 10px; font-family: monospace; font-size: 1.1em; margin: 20px 0; word-break: break-all; }
        input[type="file"] { margin: 20px 0; width: 100%; }
        button { background: #007bff; color: white; border: none; padding: 15px; border-radius: 10px; width: 100%; font-size: 16px; font-weight: bold; cursor: pointer; }
        ul { list-style: none; padding: 0; text-align: left; margin-top: 30px; }
        li { background: #fff; margin: 10px 0; padding: 15px; border-radius: 10px; border: 1px dotted #ccc; display: flex; justify-content: space-between; }
        a { text-decoration: none; color: #007bff; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📁 クラウド共有中</h2>
        <p>共有URL（見た目用）:</p>
        <div class="url-display">https://162.0.0.1:{{ port }}</div>
        
        <form method="post" enctype="multipart/form-data" action="/upload">
            <input type="file" name="file"><br>
            <button type="submit">ファイルをアップロード</button>
        </form>
        <hr>
        <h3>↓ 共有済みファイル</h3>
        <ul>
            {% for f in files %}
            <li>
                <span>{{ f }}</span>
                <a href="/download/{{ f }}" download>保存</a>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, files=files, port=DISPLAY_PORT)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '<script>alert("送信しました！"); window.location.href="/";</script>'

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    # Renderが指定するポートで通信を行う（エラー回避の肝）
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
