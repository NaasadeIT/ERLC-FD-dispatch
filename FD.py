import random
import time
import getpass
import os

class Worker:
    def __init__(self, call_sign, skills):
        self.call_sign = call_sign
        self.skills = skills
        self.busy = False

class Call:
    def __init__(self, call_id, task, skills_required, status="Pending"):
        self.call_id = call_id
        self.task = task
        self.skills_required = skills_required
        self.status = status
        self.assigned_worker = None
        self.timestamp = time.time()

calls = []
workers = []

def assign_worker(call, force_match=False, manual_assign=False):
    if manual_assign:
        available_workers = [worker for worker in workers]
    elif force_match:
        available_workers = [worker for worker in workers if not worker.busy]
    else:
        available_workers = [worker for worker in workers if not worker.busy and set(call.skills_required).issubset(set(worker.skills))]
    if available_workers:
        selected_worker = random.choice(available_workers)
        selected_worker.busy = True
        call.assigned_worker = selected_worker
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
        "SO": ("Scattered Oil", ["FIRE", "EMS"]),
        "F": ("Fall", ["EMS"])
    }
    if task_abbrev not in task_mapping:
        print("Invalid task abbreviation")
        return
    task, skills_required = task_mapping[task_abbrev]
    call = Call(call_id, task, skills_required)
    calls.append(call)
    force_match = input("Force assign a worker? (y/n): ").lower() == "y"
    assigned_worker = assign_worker(call, force_match)
    if assigned_worker is None:
        print(f"No available units for call {call.call_id} ({call.task}).")
    else:
        print(f"Call {call.call_id} ({call.task}) assigned to unit {assigned_worker.call_sign}.")
        call.status = "Assigned"

def close_call():
    print(list_calls())
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
        if call.assigned_worker:
            assigned_to = f" - Assigned to: {call.assigned_worker.call_sign}"
        else:
            assigned_to = ""
        print(f"Call {call.call_id} - {call.task} - Skills Required: {', '.join(call.skills_required)} - Status: {call.status}{assigned_to}")


def add_worker():
    call_sign = input("Enter the call sign of the unit: ")
    skills = input("Enter the skills of the unit (comma-separated): ").split(",")
    worker = Worker(call_sign, skills)
    workers.append(worker)
    print(f"Unit {call_sign} added.")

def remove_worker():
    call_sign = input("Enter the call sign of the unit to remove: ")
    for worker in workers:
        if worker.call_sign == call_sign:
            workers.remove(worker)
            print(f"Unit {call_sign} removed.")
            return
    print(f"No worker found with call sign {call_sign}.")

def list_workers():
    print("Current units:")
    for worker in workers:
        print(f"{worker.call_sign} - Skills: {', '.join(worker.skills)}")

def clear_calls():
    global calls
    calls = []
    print("All calls cleared.")

def manual_assign_call():
    print(list_calls() )
    call_id = int(input("Enter the call ID to assign a unit to: "))
    for call in calls:
        if call.call_id == call_id:
            assigned_worker = assign_worker(call, force_match=True, manual_assign=True)
            if assigned_worker is None:
                print(f"No available units for call {call.call_id} ({call.task}).")
            else:
                print(f"Call {call.call_id} ({call.task}) assigned to unit {assigned_worker.call_sign}.")
                call.status = "Assigned"
            break
    else:
        print(f"No call found with ID {call_id}.")

def logout():
    global calls, workers
    calls = []
    workers = []
    print("You have been logged out. All calls and workers have been wiped.")

def show_loading():
    print("Loading...")
    for i in range(101):
        time.sleep(0.1)
        print(f"\r{'[' + '#' * i + ' ' * (100-i) + ']'} {i}% complete", end="", flush=True)
    print()

# Define the valid ranks and corresponding welcome messages
ranks = {
    "volunteer": "Welcome, Volunteer! Please note that this system is intended for commanding officers.",
    "rookie": "Welcome, Rookie! Good luck on your first day!",
    "firefighter": "Welcome, Firefighter! Please make sure to add yourself to the system.",
    "paramedic": "Welcome, Paramedic! Remember to add yourself to the system.",
    "engineer": "Welcome, Chief! Remember to dispatch yourself too.",
    "lieutenant": "Welcome, Lieutenant! Please make sure to update the system with your unit's status.",
    "captain": "Welcome, Captain! Please make sure to update the system with the stations' status.",
    "chief": "Welcome, Chief! You have full access to all systems."
}

def login():
    print("Welcome to the Fire Department Dispatch System")
    print("Please log in to continue:")
    # Get the user's rank through a fake login prompt
    rank = getpass.getpass("Rank: ")
    # Check if the user's rank is valid and display the corresponding welcome message
    if rank.lower() in ranks:
        print(ranks[rank.lower()])
    else:
        print("Invalid rank. Access denied. You will be logged out in 3 seconds.")
        time.sleep(3)
        exit()
print(login())

time.sleep(3)
print("""\
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&#BBBBB#&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#BPY?7!!~~~!!7?YPB#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&BPY7~^^^~!7???7!~~^^~7JPB&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&#BPY?!~^~!?Y5PY55555GG5Y?7~^^!?5G#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@&BP5YYYYYYYJ?7!~^^~!?YPGGGB5..:^:.~PGGGGPY?!~^~!?Y5GB##&&&&&&@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@#5!~~~~^^^^^^~~!7?YPGGGGGGGG5..5GJ..5GGGGGGGGPY7!~^^~~!!777??JYPB&@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@BY^~~!Y555555PPGGGGGGGGGGGGG5..^!^.^PGGGGGGGGGGGGP5J?777!!!!~^^^YB@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@&&&&&@@B5!~~~JGBGGGGGGGGGGGGGGGGGG5..7:.~GGGGGGGGGGGGGGGGGGGGGGGPJ~~^!5#@@@@@@@@@@@@@@@@
    @@@@@@@@@@&BY777JP#&&BY!^^!JGGGGGGGGGGGGGGGGGGY..55..JGGGGGGGGGGGGGGGGGGGGPJ!^^!JG&@&&##&&@@@@@@@@@@
    @@@@@@@@@@#5~^~^^~?5#&&GJ!^^!YGGGGGGGGGGGGGGGB5^^5BJ^^PBGGGGGGGGGGGGGGGGP?~^^!JG&&&GY7!!7P#@@@@@@@@@
    @@@@@@@@@@BJ^~!Y7~^~75B&&GJ~^^!YGGGGGGGGGPP5YYJJ??JJ?JY55PGGGGGGGGGGGG5?~^~!YG&&#PJ!^^~~^7G@@@@@@@@@
    @@@@@@@@@@BJ^~!GG5?~^~75B&#GJ~^~75GGG5Y?!!~~~^^~~^^^~~~~~~!7?Y5GGGGG57~^~75B&&B57~^^!YJ~~!G&@@@@@@@@
    @@@@@@@@@&G7~^7GGGGP?~^~7YB&#PJ~^~7?!~^^~~~~~~~~~~~~~~~~~~~~^^~!?YY!~^~?P#&&GY7~^~7YGBY^~!G&@@@@@@@@
    @@@@@@@@@BY~~^YGGGGGGP?~^^!YB#GJ~~~^~~~~~~~~~~!!~~~~~~~!~~~~~~~~^~~~~?P#&#PJ!^^~?5GGGGY^~~P#@@@@@@@@
    @@@@@@@@#5~~^?GGGGGGGGGPJ!^~!?!~~~~~~~^^~~~~~7&G~~~~~!BB~~~~~~^~~~~~~7YG57~^^!JPGGGGGGP~~^?B@@@@@@@@
    @@@@@@@#5!~^?GGGGGGGGGGGGGJ~~^~~~~~~~!??!~!~^7&&GPPPPG&#~~~~~7P?^~~~~~~~~^~75GGGGGGGGGGJ^~~5#@@@@@@@
    @@@@@&BY~^~?GGGGGGGGGGGGGGJ~~~~~~~~~7&@@P5B~^?@B!!!!!?&#~~^!P@@Y~~~~~~~~~~5GGGGGGGGGGGGG?^~!P#@@@@@@
    @@@@&G?~^~YGGGGGGGGGGGGGG7^~~~~~~~~~7PBGP#P^^J&#PPPPPG&B~~J#BJB&!~~~~~~~~~?GGGGGGGGGGGGGG?^~!5#@@@@@
    @@@&G7^^!5GGGGGGGGGGGGGG7^~~~~~~~~~~7555PBB7^JP??JJ7!J&B!G#Y~!Y7^^^!!~~~~~^7GGGGGGGGGGGGGG?^~!5#@@@@
    @@&G7^^!PGG5?J???YGGGGG?^~~~~~~P5~~^^^^^^~5B???J~~!J7P@#B5!^^^^~7YP#&Y~~~~~^?GGGGPYYYYYYPGGJ~~~5#@@@
    @&G?^~!PGGG? .~~~7GGGGP~~~~~~^5@&GGPYJ7!~~^~J!75^~7?JYB#7!7?YPB#&@&#BP~~~~~~~5GGG5..:^:.^PGGJ~~!5#@@
    @BY~~~5GGGG?.^PGGGGGGG?^~~~~~7&&&@@@@@&B5Y?!Y~~P?^JY?YJGB&&@@&#GY?7!~~~~~~~~^7GGG5..YBY..5GGG?^~!P#@
    @G7~~7GGGGG?..^^^5GGGG!~~~~~~YP?JPG#&#PP5YJJP~!B5~??YJYYB#BBY7~~^^~~~~~~~~~~~~PGG5..^~^.^PGGGP!~^?B@
    &G7~^?GGGGG?.:YYYPGGGP~~~~~~~~^^^^~~!!YP??J5BBBGYJJJ5?JPYYJ7~^^^^^^^^~~~~~~~~~PGG5..7^ ^GGGGGG?^~!G&
    @BJ^~!PGGGG? :GGGGGGGP~~~~~~~~?Y7~~~?5PGGBGGGBGGBBBP55J5!~!?Y?JYYYJJJGB!~~~~~~PGG5..YP:.?GGGGG?^~!G&
    @&G!~^?GGGGY~!GGGGGGGG7~~~~~~~B@&BGB&@&&&@@&B#&BGPPPGGB&Y!~^!GJ&@@&&&@#!~~~~~!GGGP^^5BY^^5GGGP!~^JB@
    @@#P!~~JGGGGGGGGGGGGGGY^~~~~~~P@&&&&&&&&#5?!?#&?!!!~~YGGBP555J5@@&&&&@5^~~~~^JGGGGGGGGGGGGGGG7~~!P#@
    @@@#5!^~JGGGGGGGGGGGGGG7^~~~~~!B@&&&PYJ?!^!PB&&BPPPPG#&J5P7~~~!YP#&&@G~~~~~~!GGGGGGGGGGGGGGG?^~~5#@@
    @@@@#P!^~?GGGGGGGGGGGGGP!~~~~~~!5&@G~^^^~JBY7&&?!!!!!B&!^?G5~^~^^~P&G!~~~~~~5GGGGGGGGGGGGGP7^^!P#@@@
    @@@@@#P7^^7PGGGGGGGGGGGG5!~~~~~~^!?!~~^7GG7^7&&GPGGGG&&7~^~5BJ~~~~~7~~~~~~~YGGGGGGGGGGGGG5!^^?G&@@@@
    @@@@@@#P7^^!PGGGGGGGGGGGBP!~~~~~~~^~~~Y#Y~~~7&#7!!!!!#&7~~~^7GP!~~~~~~~~~!5GGGGGGGGGGGGGJ~^~JG&@@@@@
    @@@@@@@#P!~^7GGGGGGGGGGPY7~^~~~~~~~~~75!^~~^7&&GGPPPG&&!~~~~~~J?~~~~~~~~~JGGGGGGGGGGGGG?^~~YB@@@@@@@
    @@@@@@@@BY~~^YGGGGGGG5?~^^!J5J~~~~~~~~^~~~~~7&B!!!!!!##!~~~~~~^~~~~~~~7!^^!YPGGGGGGGGGJ^~~YB@@@@@@@@
    @@@@@@@@&G!~^JGGGGPY7~^~7YG#BP7~~^^~~~~~~~~~~7!~~~~~~77~~~~~~~~~~~~~JP#GY!^^!JPGGGGGG5~~^?B@@@@@@@@@
    @@@@@@@@&G7~^?BG5?!^^~?PB&#P?~^~7J?!~^^~~~~~~~~~~~~~~~~~~~~~~~^~~!~~!YB&&B57~^~?5GGGGJ^~!P&@@@@@@@@@
    @@@@@@@@&G!~~7Y7~^~!JG#&#P?~^~75GGGG5J?!~~^^^^~~~~~~~~~~^^~~!7J5PGY!^^!YB&&B57~^~7YGB?^~?B@@@@@@@@@@
    @@@@@@@@@G?^~~^^!?5B&&B57~^~75GGGGGGGGGGP5YJ?7777777!77??J5PGGGGGGGGY!^^!YB&&#PJ~^^!Y!~^?B@@@@@@@@@@
    @@@@@@@@@&GJ77?5G&@&BY7~^~?5GGGGGGGGGGGGGGGGGG5????JPGGGGGGGGGGGGGGGGGY!^^!YB&@#GJ!^^^^~Y#@@@@@@@@@@
    @@@@@@@@@@@&&#&@@&BY!~^~?PGGGGGGGGGGGGGGGGGGGY..~~^.^PGGGGGGGGGGGGGGGGGPJ!^^75B&@&GY777YB@@@@@@@@@@@
    @@@@@@@@@@@@@@@@&P7~~~75GGGGGGGGGGGGGGGGGGGGGJ.:PBP55GGGGGGGGGGGGGGGGGGGBGJ!^~7P#@@&&&&&@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@#5~^^~!!!!!7?JY5GGGGGGGGGGGGGJ.:PGGGGGGGGGGGGGGGGGGGPP55555Y!~^~JB@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@#PY??7777!~~^^~!7J5GGGGGGGGGJ.:PBGPPGGGGGGGGGGPY?7!~~^^^^^^~~~~YB@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@&&&&&&#BGPY?!~^^~7YPGGGGGJ..7?!:^PGGGGG5Y7!~^^~!7?JJYYYYY5PG#@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#G5?!~^~!?YPGPJ!!!!!YPPYJ7~^^~!7J5G##&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&#PY7~^^~~!7????7!~~^^~7?5GB&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&BPYJ77!!!~~!!7?YPG#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&##BBBBB#&&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """)
#ASCII ART ABOVE, DO NOT TOUCH
print("Welcome to River City's Fire Department and Emergency Medical Services Management System!")
show_loading()

def admin_calls_menu():
    while True:
        print("Call Administration Options:")
        print("1. Add call")
        print("2. Close call")
        print("3. List calls")
        print("4. Assign unit manually")
        print("Q. Quit Call Administration")
        choice = input("Enter your choice: ").lower()
        if choice == "1":
            add_call()
        elif choice == "2":
            close_call()
        elif choice == "3":
            list_calls()
        elif choice == "4":
            manual_assign_call()
        elif choice == "q":
            print("Exiting Call Administration Menu...")
            break
        else:
            print("Invalid choice.")

def admin_workers_menu():
    while True:
        print("Worker Administration Options:")
        print("1. Add unit")
        print("2. Remove unit")
        print("3. List units")
        print("Q. Quit Worker Administration")
        choice = input("Enter your choice: ").lower()
        if choice == "1":
            add_worker()
        elif choice == "2":
            remove_worker()
        elif choice == "3":
            list_workers()
        elif choice == "q":
            print("Exiting Worker Administration Menu...")
            break
        else:
            print("Invalid choice.")

def main_menu():
    while True:
        print("Main Menu:")
        print("1. Call Administration")
        print("2. Worker Administration")
        print("3. Logout")
        print("Q. Quit the program")
        choice = input("Enter your choice: ").lower()
        if choice == "1":
            admin_calls_menu()
        elif choice == "2":
            admin_workers_menu()
        elif choice == "3":
            logout()
            break
        elif choice == "q":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice.")
print(main_menu())