from flask import Flask, request, render_template, send_file, redirect, url_for
from flask_socketio import SocketIO, emit
import gxzf
import threading

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        base_url = url + '{}'
        thread = threading.Thread(target=run_gxzf, args=(base_url,))
        thread.start()
        return redirect(url_for('progress'))

    return render_template('index.html')

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/download')
def download_file():
    return send_file('gxzf.xlsx', as_attachment=True)

def run_gxzf(url):
    gxzf.run(url, socketio)
    socketio.emit('task_complete', {'data': 'Task completed'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
