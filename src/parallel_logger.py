# from queue import Queue

# log_queue = Queue()


# def log(message: str):
#     log_queue.put(message)


# def write_log():
#     while True:
#         msg = log_queue.get()
#         print(msg)


# from concurrent.futures.thread import ThreadPoolExecutor

# executor = ThreadPoolExecutor(1)

# def log(message:str):
#     executor.submit(print, message)


import threading


def log(message: str):
    t = threading.Thread(target=lambda: print(message))
    t.start()


# import logging

# def log(message: str):
#     logging.info(message)
