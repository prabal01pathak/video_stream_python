#from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import Queue, cpu_count, Process
import time

def do_work(queue, x):
    print('{} started'.format(x))
    z = 10
    data = {
        "x": x,
        "y": x * x
    }
    queue.put(data)
    time.sleep(1)
    z -= 1
    #return x * x

def read_queue(queue):
    while True:
        try:
            while queue.empty():
                data = queue.get()
                print('{} finished'.format(data))
        except KeyboardInterrupt:
            break
def fill_queue(queue):
    for x in range(1, 10):
        p = Process(target=do_work, args=(queue, x))
        p.start()

def main():
    queue = Queue()
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(do_work, i) for i in range(10)]
        for future in as_completed(futures):
            print(future.result())
    #p2 = Process(target=read_queue, args=(queue,))
    #i = 10
    #p = Process(target=do_work, args=(queue, i))
    #p2 = Process(target=read_queue, args=(queue,))
    #p.start()
    #p2.start()
    #p.join()
    #p2.join()

i = 10

def worker(queue):
    global i
    while True:
        try:
            i -= 1
            print('{} started'.format(i))
            data = {
                "x": i,
                "y": i * i
            }
            queue.put(data)
        except KeyboardInterrupt:
            break

def reader(queue):
    while True:
        try:
            while queue.empty():
                data = queue.get()
                print('{} finished'.format(data))
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    #main()
    queue = Queue()
    p1 = Process(target=worker, args=(queue,))
    p2 = Process(target=reader, args=(queue,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

