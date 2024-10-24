from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import yt_dlp
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    response = requests.get(url)
    url = response.url
    if url:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)

            # ダウンロード完了メッセージとリンクを表示
            return f"<h2>ダウンロード完了</h2><a href='{url_for('download_file', filename=os.path.basename(filename))}'>url</a>"
        except Exception as e:
            return f"Error: {str(e)}"
    return redirect(url_for('index'))

@app.route('/downloads/<path:filename>')
def download_file(filename):
    file_path = os.path.join('downloads', filename)
    response = send_from_directory('downloads', filename, as_attachment=True)
    
    # ダウンロード後にファイルを削除
    
    return response

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(host='10.7.48.56', port=5000)
