import socket
import sys
import threading
import time
try:
    import readline # For command line input
except ImportError:
    pass

with open("actions.txt", "r") as file:
    ACTIONS = file.read().strip() + "\n" # Ensure there's a newline at the end
ACTIONS = ACTIONS.encode("utf-8") # Encode the actions to bytes

commands = {} # Dictionary to hold commands for each thread

def run_thread(name):
    protocol = sys.argv[3] if len(sys.argv) > 3 else "v4" # Protocol, default to IPv4
    if protocol == "v6": # Check if IPv6 is specified
        ADDRESS = (sys.argv[1], int(sys.argv[2]), 0, 0) # IPv6 address format
        PROTOCOL = socket.AF_INET6 # Use IPv6 socket
    else:
        ADDRESS = (sys.argv[1], int(sys.argv[2])) # IPv4 address format
        PROTOCOL = socket.AF_INET # Use IPv4 socket
    try:
        with socket.socket(PROTOCOL, socket.SOCK_STREAM) as s: # Create a socket
            s.connect(ADDRESS) # Connect to the server
            print(f"Thread {name} initialized.")
            flood(name, s) # and start flooding!
    except OSError as e:
        print(f"{e.__class__.__name__} in thread {name}: {e}") # Handle socket errors
        time.sleep(10) # Wait before retrying
        run_thread(name) # and retry


def flood(name, sock):
    i = 0 # Number of action sets sent
    while True: # Infinite loop to keep sending actions
        if name in commands: # Check if there are commands for this thread
            sock.send(commands[name].encode("utf-8")) # Send the command
            del commands[name] # Remove the command after sending to avoid re-sending
        sock.send(ACTIONS) # Send the action set
        i += 1 # Increment the action set counter
        if i % 1e3 == 0: # Print every 1000 action sets
            print(f"Thread {name} processed {i} action sets.")
        if stop: # Check if the stop flag is set
            print(f"Thread {name} stopping.")
            break


stop = False # Dont't stop at beginning; init variable
names = range(3) # 3 threads fill 1GBit/s uplink, for me
threads = [threading.Thread(target=run_thread, args=(name,)) for name in names] # Create threads for each name
for thread in threads:
    thread.start() # Start all threads
    time.sleep(0.01) # Small delay, sending the pixel 3 times in a row, doesn't work so good
while True:
    try:
        action = input("> ").strip() # Get user input for action
    except (KeyboardInterrupt, EOFError): # Handle exit signals
        print("Exiting...")
        break
    action_split = action.split(" ") # Split the action into command and arguments
    command = None # no default command
    action = action_split[0] # First part is the action
    args = action_split[1:] # Remaining parts are arguments
    if action in ["stop", "exit", "quit"]: # Check for exit commands
        break
    elif action == "help": # Show help message
        print("Available actions: quit (stop, exit), help, offset (of), raw")
        print("Enter the action followed by arguments.")
        print("Example: offset 10 20")
        print("For help, enter just the action.")
        continue
    elif action == ["offset", "of"]: # Check for offset command
        if len(args) != 2:
            print("Usage: offset <x> <y>")
            continue
        try:
            args = [int(arg) for arg in args] # Convert arguments to integers
        except ValueError:
            print("Need integers for offset")
            continue
        command = f"OFFSET {args[0]} {args[1]}"
    elif action == "raw": # Check for raw command
        if len(args) < 1:
            print("Usage: raw <command>")
            continue
        command = " ".join(args)
    else: # If action is not recognized
        print(f"Unknown action: {action}")
        continue
    if command:
        for name in names: # Assign the action to each thread
            commands[name] = f"{command}\n"
stop = True # At the end, set the stop flag to true
for thread in threads: # Wait for all threads to finish
    thread.join()
