import os
import threading
from flask import Flask, render_template, request, send_from_directory, jsonify, abort
from werkzeug.utils import secure_filename
from Program import Process, release_resources, video_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

process_thread = None
thread_lock = threading.Lock()

def start_process_thread(filename):
    global process_thread
    with thread_lock:
        if process_thread is None or not process_thread.is_alive():
            process_thread = threading.Thread(target=Process, args=(filename,))
            process_thread.start()

def stop_process_thread():
    global process_thread
    with thread_lock:
        if process_thread is not None and process_thread.is_alive():
            release_resources()
            process_thread.join()
            process_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify(message="No video file provided"), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify(message="No selected file"), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    start_process_thread(filepath)
    return jsonify(message="Video uploaded and processing started.", filename=filename)

@app.route('/download-video/<filename>')
def download_video(filename):
    try:
        response = send_from_directory(directory='uploads', path=filename, as_attachment=True, mimetype='video/x-msvideo')
        # Reset the state of the webpage after download
        stop_process_thread()
        return response
    except Exception as e:
        print(f"Error serving video file: {e}")
        abort(500)

@app.route('/reset', methods=['POST'])
def reset():
    # Release resources and reset the state
    stop_process_thread()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
