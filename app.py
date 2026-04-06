import os, random, socket
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 表示用のランダムポートを事前に生成
current_display_port = random.randint(1024, 65535)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Share</title>
    <style>
        body { font-family: sans-serif; padding: 20px; text-align: center; background: #f0f4f8; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .url-box { background: #eee; padding: 10px; border-radius: 5px; font-weight: bold; color: #d63384; word-break: break-all; }
        input[type="file"] { margin: 20px 0; width: 100%; }
        button { background: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 8px; width: 100%; font-size: 16px; }
        ul { list-style: none; padding: 0; text-align: left; margin-top: 20px; }
        li { background: #fff; margin: 5px 0; padding: 12px; border-radius: 8px; border: 1px solid #ddd; }
        a { text-decoration: none; color: #007bff; }
    </style>
</head>
<body>
    <div class="card">
        <h2>📁 ファイル共有</h2>
        <p>共有用URL:</p>
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
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML, files=files, ip=get_local_ip(), port=current_display_port)

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
    # Render等のサーバーが指定するポートを優先し、なければ10000番を使用
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
