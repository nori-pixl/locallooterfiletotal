import os, random, socket
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 自分のローカルIP（192.168.x.x）を取得する関数
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
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Share</title></head>
<body>
    <h2>📁 ルーター内ファイル共有</h2>
    <p>現在のURL: <b>https://{{ ip }}:{{ port }}</b></p>
    <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="file"><button type="submit">送信</button>
    </form>
    <hr>
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
    return render_template_string(HTML, files=files, ip=get_local_ip(), port=current_port)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file: file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '<script>location.href="/";</script>'

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    # 1024〜65535でランダムなポートを決定
    current_port = random.randint(1024, 65535)
    app.run(host='0.0.0.0', port=current_port)
