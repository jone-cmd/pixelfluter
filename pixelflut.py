import socket
import sys
import threading
import time

with open("actions.txt", "r") as file:
    ACTIONS = file.read().strip() + "\n"
ACTIONS = ACTIONS.encode("utf-8")

ADDRESS = (sys.argv[1], int(sys.argv[2]))

commands = {}

def run_thread(name):
    protocol = sys.argv[3] if len(sys.argv) > 3 else "v4"
    if protocol == "v6":
        ADDRESS = (sys.argv[1], int(sys.argv[2]), 0, 0)
        PROTOCOL = socket.AF_INET6
    else:
        ADDRESS = (sys.argv[1], int(sys.argv[2]))
        PROTOCOL = socket.AF_INET
    try:
        with socket.socket(PROTOCOL, socket.SOCK_STREAM) as s:
            s.connect(ADDRESS)
            print(f"Thread {name} initialized.")
            flood(name, s)
    except OSError as e:
        print(f"{e.__class__.__name__} in thread {name}: {e}")
        time.sleep(10)
        run_thread(name)


def flood(name, sock):
    i = 0
    while True:
        if name in commands:
            sock.send(commands[name].encode("utf-8"))
            del commands[name]
        sock.send(ACTIONS)
        i += 1
        if i % 1e3 == 0:
            print(f"Thread {name} processed {i} action sets.")
        if stop:
            print(f"Thread {name} stopping.")
            break
    sock.close()


stop = False
names = range(3)
threads = [threading.Thread(target=run_thread, args=(name,)) for name in names]
for thread in threads:
    thread.start()
    time.sleep(0.01)
while True:
    try:
        action = input("> ")
    except (KeyboardInterrupt, EOFError):
        print("Exiting...")
        break
    for name in names:
        commands[name] = f"{action}\n"
stop = True
for thread in threads:
    thread.join()
