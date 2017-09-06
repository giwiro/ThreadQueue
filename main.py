import urllib3
import time
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup

urllib3.disable_warnings()

num_threads = 8;
q = Queue()
out = Queue()
hosts = ["http://google.com", "http://amazon.com", "http://ibm.com", "http://apple.com"]
http = urllib3.PoolManager()
start = time.time()

def worker(queue):
    while True:
        host = queue.get()
        if host is None:
            break
        r = http.request("GET", host)
        out.put(r.data)
        queue.task_done()

def out_worker(queue):
    while True:
        data = queue.get()
        if data is None:
            break
        soup = BeautifulSoup(data, "html.parser")
        print(soup.find('title'))
        queue.task_done()

for i in range(num_threads):
    t = Thread(target=worker, args=(q,))
    t.daemon = True
    t.start()


for host in hosts:
    q.put(host)


for i in range(num_threads):
    t = Thread(target=out_worker, args=(out,))
    t.daemon = True
    t.start()

q.join()
out.join()
print("Elapsed Time: %s" % (time.time() - start))
