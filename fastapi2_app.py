from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor
import time

app = FastAPI()

class Worker:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.value = True
        self.queue = Queue()
        self.item_value = 0 
        self.thread_value = 0

    def __repr__(self):
        return f"Worker(name={self.name}, age={self.age})"

    def do_work(self, thread_name):
        while self.value:
            self.item_value += 1
            print(f"{thread_name} is working")

    def do_work_with_queue(self, queue):
        while True:
            print(f"{self.name} is working")
            queue.put(f"{self.name} is working")
            time.sleep(1)

    def thread_work_do_work(self, thread_name):
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.do_work, thread_name)

    def yield_item_value(self):
        while True:
            yield self.item_value

    def modify_value(self, value):
        self.value = value

worker = Worker("John", 30)

@app.get("/")
async def root(request: Request):
    return JSONResponse({"message": "Hello World"})

@app.get("/worker")
async def worker_app(request: Request, background_task: BackgroundTasks):
    worker.thread_value += 1
    background_task.add_task(worker.thread_work_do_work, f"Thread-{worker.thread_value}")
    return JSONResponse({"message": "Hello World"})

@app.get("/yield")
async def yield_item_value(request: Request):
    return worker.yield_item_value()

@app.get("/modify_value")
async def modify_value(request: Request):
    if worker.value:
        worker.value = False
        return JSONResponse({"message": "Value is False"})
    else:
        worker.value = True
        return JSONResponse({"message": "Value is True"})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # revieve message from client as json
        data = await websocket.receive_json()
        print(data)
        if data['action'] == 'start':
            for frame in worker.yield_item_value():
                await websocket.send_json(frame)
        elif data['action'] == 'stop':
            await websocket.send_json({'action': 'stop'})
            break
        else:
            await websocket.send_json({'action': 'unknown'})

if __name__ == "__main__":
    import uvicorn
    # run with reload
    uvicorn.run(app, reload=True)
