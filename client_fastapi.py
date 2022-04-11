import websocket
import rel
import json
from threading import Thread
import cv2
import base64
import numpy as np

def on_message(ws, message):
    data = json.loads(message)
    print(data)

def show_image_data(data):
    if isinstance(data, dict):
        image = base64.b64decode(data['frame'])
        npimg = np.fromstring(image, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        # write frame to file
        #cv2.imwrite('frame.jpg', frame)
        #frame = cv2.imread('frame.jpg')
        try:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                ws.close()
        except:
            pass

def show_image():
    while True:
        try:
            frame = cv2.imread('frame.jpg')
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass

def on_open(ws):
    print("open")
    ws.send(json.dumps({"action":"start"}))

def on_stream(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def send_ws(ws, message):
    ws.send(json.dumps(message))

def connect_websocket(url):
    global ws
    print(url)
    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_open=on_open)
    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()

connect_websocket('ws://localhost:8000/ws')
#thread = Thread(target=connect_websocket, args=("ws://localhost:8000/ws",))
#thread.start()

try:
    pass
except KeyboardInterrupt:
    ws.close()
    thread.join()
