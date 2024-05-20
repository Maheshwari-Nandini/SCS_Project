import threading
from flask import Flask, render_template, send_from_directory, jsonify, abort
from Program import Process, stop_process, video_filename

app = Flask(__name__)

process_thread = None
thread_lock = threading.Lock()

def start_process_thread():
    global process_thread
    with thread_lock:
        if process_thread is None or not process_thread.is_alive():
            process_thread = threading.Thread(target=Process)
            process_thread.start()

def stop_process_thread():
    global process_thread
    with thread_lock:
        if process_thread is not None and process_thread.is_alive():
            stop_process()
            process_thread.join()
            process_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loadP')
def loadP():
    start_process_thread()
    return jsonify(message="Video processing started.", filename=video_filename)

@app.route('/stop')
def stop():
    stop_process_thread()
    return jsonify(message="Video processing stopped.", filename=video_filename)

@app.route('/download-video/<filename>')
def download_video(filename):
    try:
        return send_from_directory(directory='uploads', path=filename, as_attachment=True)
    except Exception as e:
        print(f"Error serving video file: {e}")
        abort(500)  # Use abort function to return a 500 Internal Server Error response

if __name__ == '__main__':
    app.run(debug=True)