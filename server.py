import os
import http.server
import socketserver
import webbrowser

# サーバーの設定
PORT = 8000  # 使用するポート番号

# スクリプトのディレクトリに移動
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

# サーバーハンドラを定義
Handler = http.server.SimpleHTTPRequestHandler

# サーバーを起動
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    print(f"Serving files from: {script_directory}")
    
    # デフォルトブラウザでページを開く
    webbrowser.open(f"http://localhost:{PORT}")
    
    # サーバーを起動し続ける
    httpd.serve_forever()
