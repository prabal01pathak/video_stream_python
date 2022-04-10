from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from typing import List, Optional
import asyncio
import cv2

app = FastAPI()

app.on_event("startup")(lambda: print("App started"))


def stream_video(video_path):
    cap = cv2.VideoCapture(video_path)
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

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/stream")
def stream(request: Request, response: Response):
    return StreamingResponse(stream_video(0), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000)
