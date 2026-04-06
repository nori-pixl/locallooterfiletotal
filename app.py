import os
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 共有画面のデザイン
BASE_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>File Share</title></head>
<body>
    <h2>📁 ファイル共有中</h2>
    <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="file"><button type="submit">送信</button>
    </form>
    <hr>
    <h3>共有済みリスト</h3>
    <ul>
        {% for f in files %}
        <li><a href="/download/{{ f }}" download>{{ f }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(BASE_HTML, files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file and file.filename:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '<script>location.href="/";</script>'

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    import random
    # サーバー起動時にランダムなポートを割り当てる（ローカル実行用）
    port = random.randint(1024, 65535)
    app.run(host='0.0.0.0', port=port)
