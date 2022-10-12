import time
import threading
import requests
import json
import cooks
import menu
import order_in
import order_out
from wsgiref.simple_server import make_server

def K_App(environment, response):
    status = '200 OK'
    headers = [('content-type', 'text/html; charset=utf-8')]
    response(status, headers)
    return [b'<h2>Kitchen server</h2>']


with make_server('', 3501, K_App) as server:
    print('serving on port 3501...\nvisit http://127.0.0.1:3501\nTo exit press ctrl + c')
    server.serve_forever()

q = []
st = []

@K_App.put("/put")

## get http put request from the dinning hall
def get_order():
    global q
    mutex = threading.Lock()
    ## do while dinning hall is generating order requests
    while requests.get("http://127.0.0.1:3501/put") != {"state": "no more incoming orders"}:
        ## lock
        mutex.acquire()
        resp = requests.get("http://127.0.0.1:3501/put")
        received_order = json.loads(resp, object_hook=order_in.orderIn)
        ## add received order to queue
        q.append(received_order)
        ## unlock
        mutex.release()

## cook orders
def cook_order():
    global q
    global st
    for i in range(len(q)):
        cooking_det = []
        for k in range(len(q[i].items)):
            for l in range(len(cooks.cooks)):
                ## food items cooked by relevant cooks according to complexity of food and cook's rank
                if (cooks.cooks[l].rank == menu.menu[q[i].items[k]].complexity) or (cooks.cooks[l].rank > menu.menu[q[i].items[k]].complexity):
                    cook_name = cooks.cooks[l].name
                    food_item = q[i].items[k]
                    ## actually cooking food
                    time.sleep(menu.menu[q[i].items[k]].prep_time*0.1)
                    ## recording cooking details
                    food_item_c_det = order_out.c_det(food_item, cook_name)
                    cooking_det.append(food_item_c_det)
        cooking_time = q[i].max_wait + 5
        ## order to be sent back to dinning hall
        order_cooked = order_out(q[i].order_id, q[i].table_id, q[i].waiter_id, q[i].priority, q[i].items, q[i].max_wait, q[i].pick_up_time, cooking_time, cooking_det)
        st.append(order_cooked)

## send cooked orders back to the dinning hall via http put
def send_order():
    global st
    mutex = threading.Lock()
    ## do while stack is not empty
    while len(st) > 0:
        ## lock
        mutex.acquire()
        pick_up_cooked_order = st.pop()
        order_to_json = json.dumps(pick_up_cooked_order.__dict__)
        requests.put("http://127.0.0.1:3500/put", json=order_to_json)
        ## unlock
        mutex.release()
    if len(st) == 0:
        requests.put("http://127.0.0.1:3500/put", json={"state": "all orders have been cooked"})

## multiple waiters threads
waiters = [threading.Thread(target=send_order) for i in range(4)]

if __name__ == '__main__':
    ## start waiters multithreading
    for waiter in waiters:
        waiter.start()
    ## run kitchen server
    K_App.run(host='localhost', port=3501)
