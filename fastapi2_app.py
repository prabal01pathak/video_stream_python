from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
from feed_logic.saved_driver import main

app = FastAPI()

class Worker:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.value = True
        self.queue = Queue()
        self.item_value = 0 
        self.thread_value = 0
        self.queue.put({"value": self.value})
        self.processed_frame = None

    def __repr__(self):
        return f"Worker(name={self.name}, age={self.age})"

    def do_work(self, thread_name):
        while self.value:
            self.item_value += 1
            print(f"{thread_name} is working")
            time.sleep(0.01)

    def do_work_with_queue(self, queue):
        print("do_work_with_queue")
        #while self.value:
        #    print(f"{self.name} is working")
        #    while not queue.empty():
        #        item = queue.get()
        #        self.break_value = item["value"]
        #        print(self.break_value)
        #        if not self.break_value:
        #            break
        #    queue.put(f"{self.name} is working")
        #    time.sleep(1)

    def thread_worker(self, thread_name):
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.do_work, thread_name)

    def process_worker(self, queue):
        with ProcessPoolExecutor(max_workers=1) as executor:
            executor.submit(self.do_work_with_queue, queue)

    def call_main(self):
        main(processed_frame = self.processed_frame)

    def yeild_processed_frames():
        """Yeilds processed frames

        Returns:
            [ndarray]: Processed frame
        """
        while True:
            yield self.processed_frame

    def yield_item_value(self):
        while True:
            yield self.item_value

    def modify_value(self, value):
        self.value = value

    def modify_queue(self, queue):
        self.value = False
        self.queue.put({"value": self.value})


worker = Worker("John", 30)

@app.get("/")
async def root(request: Request):
    return JSONResponse({"message": "Hello World"})

@app.get("/worker")
async def worker_app(request: Request, background_task: BackgroundTasks):
    worker.thread_value += 1
    #background_task.add_task(worker.thread_worker, f"Thread-{worker.thread_value}")
    background_task.add_task(worker.call_main)
    return JSONResponse({"message": "Hello World"})

@app.get("/process")
async def process_app(request: Request, background_task: BackgroundTasks):
    #worker.process_worker(worker.queue)
    background_task.add_task(worker.process_worker, worker.queue)
    return JSONResponse({"message": "Hello World"})

@app.get("/yield")
async def yield_item_values(request: Request):
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
            for frame in worker.yield_processed_frame():
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
