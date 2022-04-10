import cv2
from flask import Flask, render_template, Response, jsonify
from flask import Response
import os

cap = cv2.VideoCapture(0)

def stream_video(video_path):
    while True:
        ret, frame = cap.read()
        if ret:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            data = {
                'frame': cv2.imencode('.jpg', frame)[1].tobytes(),
            }
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data['frame'] + b'\r\n\r\n')
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def print_stream():
    for frame in stream_video(0):
        print(frame.shape)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

@app.route('/stream')
def video_feed():
    return Response(stream_video(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stop_server")
def stop_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(port=8000, debug=True)
