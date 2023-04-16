import random
import time

class Worker:
    def __init__(self, call_sign, skills):
        self.call_sign = call_sign
        self.skills = skills

class Call:
    def __init__(self, call_id, task, skills_required, status="Pending"):
        self.call_id = call_id
        self.task = task
        self.skills_required = skills_required
        self.status = status

calls = []
workers = []

def assign_worker(call):
    available_workers = [worker for worker in workers if set(call.skills_required).issubset(set(worker.skills))]
    if available_workers:
        selected_worker = random.choice(available_workers)
        return selected_worker
    else:
        return None

def add_call():
    call_id = len(calls) + 1
    task_abbrev = input("Enter the task abbreviation (e.g. GSE for Gas Station Explosion): ")
    task_mapping = {
        "GSE": ("Gas station explosion", ["FIRE"]),
        "BC": ("Bridge Collapse", ["FIRE", "EMS"]),
        "MVA": ("Motor Vehicle Accident", ["FIRE", "EMS"]),
        "PC": ("Plane Crash", ["FIRE", "EMS"]),
        "SW": ("Strong Winds", ["FIRE", "EMS"]),
        "TC": ("Tunnel Collapse", ["FIRE", "EMS"]),
        "OS": ("Oil Spill", ["FIRE"]),
        "CS": ("Chemical Spill", ["HAZMAT"]),
        "BBF": ("Building-Bush Fire", ["FIRE"]),
        "ALI": ("Arm-Leg Injury", ["EMS"]),
        "SHA": ("Stroke-Heart Attack", ["EMS"]),
        "SO": ("Scattered Oil", ["FIRE", "EMS"])
    }
    if task_abbrev not in task_mapping:
        print("Invalid task abbreviation")
        return
    task, skills_required = task_mapping[task_abbrev]
    call = Call(call_id, task, skills_required)
    calls.append(call)
    assigned_worker = assign_worker(call)
    if assigned_worker is None:
        print(f"No available workers for call {call.call_id} ({call.task}).")
    else:
        print(f"Call {call.call_id} ({call.task}) assigned to worker {assigned_worker.call_sign}.")
        call.status = "Assigned"
    
def close_call():
    call_id = int(input("Enter the call ID to close: "))
    for call in calls:
        if call.call_id == call_id:
            call.status = "Closed"
            print(f"Call {call_id} ({call.task}) closed.")
            return
    print(f"No call found with ID {call_id}.")

def list_calls():
    print("Current calls:")
    for call in calls:
        print(f"Call {call.call_id} - {call.task} - Skills Required: {', '.join(call.skills_required)} - Status: {call.status}")

def add_worker():
    call_sign = input("Enter the call sign of the worker: ")
    skills = input("Enter the skills of the worker (comma-separated): ").split(",")
    worker = Worker(call_sign, skills)
    workers.append(worker)
    print(f"Worker {call_sign} added.")

def remove_worker():
    call_sign = input("Enter the call sign of the worker to remove: ")
    for worker in workers:
        if worker.call_sign == call_sign:
            workers.remove(worker)
            print(f"Worker {call_sign} removed.")
            return
    print(f"No worker found with call sign {call_sign}.")

def list_workers():
    print("Current workers:")
    for worker in workers:
        print(f"{worker.call_sign} - Skills: {', '.join(worker.skills)}")

def clear_calls():
    global calls
    calls = []
    print("All calls cleared.")

def show_loading():
    print("Loading...")
    for i in range(101):
        time.sleep(0.1)
        print(f"\r{'[' + '#' * i + ' ' * (100-i) + ']'} {i}% complete", end="", flush=True)
    print()

print("Welcome to Emergency Services Management System")
show_loading()

while True:
    print("Enter an option:")
    print("1. Add a call")
    print("2. Close a call")
    print("3. List current calls")
    print("4. Add a worker")
    print("5. Remove a worker")
    print("6. List all workers")
    print("7. Clear all calls")
    user_input = input(">> ")
    if user_input == "1":
        add_call()
    elif user_input == "2":
        close_call()
    elif user_input == "3":
        list_calls()
    elif user_input == "4":
        add_worker()
    elif user_input == "5":
        remove_worker()
    elif user_input == "6":
        list_workers()
    elif user_input == "7":
        clear_calls()
    else:
        print("Invalid option.")