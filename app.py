import os, random, socket
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'my_shared_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 自分のスマホのローカルIPを取得
def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# 画面のデザイン
HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Local Share</title></head>
<body style="text-align:center; font-family:sans-serif; padding:20px;">
    <h2>📱 スマホ直結シェア</h2>
    <p>相手はこのURLをブラウザに入力してください：</p>
    <div style="background:#eee; padding:10px; font-weight:bold; color:red;">http://{{ ip }}:{{ port }}</div>
    <hr>
    <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="file"><br><br>
        <button type="submit" style="padding:10px 20px;">アップロード</button>
    </form>
    <hr>
    <h3>共有済みファイル</h3>
    <ul style="text-align:left;">
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
    return render_template_string(HTML, files=files, ip=get_my_ip(), port=current_port)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file: file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return '<script>alert("完了！"); location.href="/";</script>'

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    # 起動するたびにランダムなポートを選択
    current_port = random.randint(1024, 65535)
    print(f"\n🚀 サーバー起動中！")
    print(f"相手に教えるURL: http://{get_my_ip()}:{current_port}")
    # スマホ本体で待ち受け開始
    app.run(host='0.0.0.0', port=current_port)
