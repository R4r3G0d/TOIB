import requests
import threading

def increment_counter():
    response = requests.post('http://localhost:5000/increment')
    print(response.text)

threads = []
for i in range(1000):
    t = threading.Thread(target=increment_counter)
    q = threading.Thread(target=increment_counter)
    threads.append(t)
    threads.append(q)
    t.start()
    q.start()

for t in threads:
    t.join()