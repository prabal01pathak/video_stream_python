from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from fastapi.websockets import WebSocket
from typing import List, Optional
import asyncio
import cv2
import json
import base64

app = FastAPI()

app.on_event("startup")(lambda: print("App started"))

cap = cv2.VideoCapture(0)
def stream_video(video_path):
    while True:
        ret, frame = cap.read()
        if ret:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            data = {
                'frame': cv2.imencode('.jpg', frame)[1].tobytes(),
                'success': True
            }
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + data['frame'] + b'\r\n\r\n')
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def stream_video_dict(video_path):
    while True:
        ret, frame = cap.read()
        if ret:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            frame = cv2.imencode('.jpg', frame)[1].tobytes(),
            # get only frame from the tuple
            frame = frame[0]
            encoded_frame = base64.b64encode(frame).decode('utf-8')
            data = {
                'success': True,
                'frame': encoded_frame
            }
            yield data
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/stream")
def stream(request: Request, response: Response):
    return StreamingResponse(stream_video(0), media_type='multipart/x-mixed-replace; boundary=frame')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # revieve message from client as json
        data = await websocket.receive_json()
        print(data)
        if data['action'] == 'start':
            for frame in stream_video_dict(0):
                print(type(frame))
                await websocket.send_json(frame)
        elif data['action'] == 'stop':
            await websocket.send_json({'action': 'stop'})
            break
        else:
            await websocket.send_json({'action': 'unknown'})
        # stream a response to the client type json with generator
        #await websocket.send_json(stream_video_dict(0))
        #await websocket.send_bytes(stream_video_dict(0))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000)
