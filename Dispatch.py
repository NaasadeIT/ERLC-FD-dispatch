#Imports all needed modules
import random
import time
import getpass
import os

#Defines the class for the worker
class Worker:
    def __init__(self, call_sign, team):
        self.call_sign = call_sign
        self.team = team.split("-")
        self.busy = False

#Defines the class for the call
class Call:
    def __init__(self, call_id, task, teams_required, status="Pending"):
        self.call_id = call_id
        self.task = task
        self.teams_required = teams_required
        self.status = status
        self.assigned_worker = []
        self.timestamp = time.time()

#empty lists for calls and workers
calls = []
workers = []

# Dictionary of possible calls
task_mapping = {
    "GSE": ("Gas station explosion", "FIRE"),
    "BC": ("Bridge Collapse", "FIRE-EMS"),
    "MVA": ("Motor Vehicle Accident", "FIRE-EMS"),
    "PC": ("Plane Crash", "FIRE-EMS"),
    "SW": ("Strong Winds", "FIRE-EMS"),
    "TC": ("Tunnel Collapse", "FIRE-EMS"),
    "OS": ("Oil Spill", "FIRE"),
    "CS": ("Chemical Spill", "HAZMAT"),
    "BBF": ("Building-Bush Fire", "FIRE"),
    "ALI": ("Arm-Leg Injury", "EMS"),
    "SHA": ("Stroke-Heart Attack", "EMS"),
    "SO": ("Scattered Oil", "FIRE-EMS"),
    "F": ("Fall", "EMS")
}

#Defines the function to assign a worker to a call
def assign_worker(call, force_match=False, manual_assign=False):
    required_teams = call.teams_required.split("-")
    num_teams_required = len(required_teams)
    if manual_assign:
        available_workers = [worker for worker in workers]
    elif force_match:
        available_workers = [worker for worker in workers if not worker.busy]
    else:
        available_workers = [worker for worker in workers if not worker.busy and any(team in required_teams for team in worker.team)]
    if num_teams_required == 1:
        num_workers = 1
    elif num_teams_required == 2:
        num_workers = 2
    else:
        # More than two teams required, can't handle the call
        return []
    if len(available_workers) >= num_workers:
        selected_workers = random.sample(available_workers, num_workers)
        for selected_worker in selected_workers:
            selected_worker.busy = True
            call.assigned_worker.append(selected_worker)  # update the assigned_worker attribute of the call
        if len(selected_workers) == num_workers:
            return selected_workers
        else:
            # There are not enough workers available to handle the call
            return []
    else:
        # There are not enough workers available to handle the call
        return []
    
#CALL FUNCTIONS BEGIN HERE
    
#Defines the function to add a call
def add_call():
    call_id = len(calls) + 1
    task_abbrev = input("Enter the task abbreviation (e.g. GSE for Gas Station Explosion): ")
    if task_abbrev not in task_mapping:
        print("Invalid task abbreviation")
        return
    task, team_required = task_mapping[task_abbrev]
    call = Call(call_id, task, team_required)
    calls.append(call)
    force_match = input("Force assign a worker? (y/n): ").lower() == "y"
    assigned_worker = assign_worker(call, force_match)
    if not assigned_worker:
        print(f"No available units for call {call.call_id} ({call.task}).")
    else:
        print(f"Call {call.call_id} ({call.task}) assigned to unit(s) {', '.join([worker.call_sign for worker in assigned_worker])}.")
        call.status = "Assigned"

#Defines the function to close a call
def close_call():
    print(list_calls())
    call_id = int(input("Enter the call ID to close: "))
    for call in calls:
        if call.call_id == call_id:
            call.status = "Closed"
            for team in call.teams_required.split("-"):
                workers_with_team = [worker for worker in workers if team in worker.team and not worker.busy]
                if not workers_with_team:
                    print(f"No available units for team {team} for call {call.call_id} ({call.task}).")
                    break
                selected_worker = random.choice(workers_with_team)
                selected_worker.busy = True
                call.assigned_worker.append(selected_worker)  # update the assigned_worker attribute of the call
            else:
                assigned_workers = ", ".join([worker.call_sign for worker in call.assigned_worker])
                print(f"Call {call.call_id} ({call.task}) closed. Assigned to {assigned_workers}")
                for assigned_worker in call.assigned_worker:
                    assigned_worker.busy = True
            break
    else:
        print("Invalid call ID.")

#Defines the function to list the calls
def list_calls():
    print("Current calls:")
    for call in calls:
        if call.assigned_worker:
            assigned_to = " - Assigned to: "
            for worker in call.assigned_worker:
                assigned_to += worker.call_sign + ", "
            assigned_to = assigned_to[:-2]  # remove the last comma and space
        else:
            assigned_to = ""
        print(f"Call {call.call_id} - {call.task} - Teams Required: {''.join(call.teams_required)} - Status: {call.status}{assigned_to}")

#Allows the user to manually assign a call
def manual_assign_call():
    print(list_calls())
    call_id = int(input("Enter the call ID to assign a unit to: "))
    worker_id = input("Enter the worker ID to assign to the call: ")
    for call in calls:
        if call.call_id == call_id:
            assigned_worker = assign_worker(call, force_match=True, manual_assign=True)
            if assigned_worker is None:
                print(f"No available units for call {call.call_id} ({call.task}).")
            else:
                print(f"Call {call.call_id} ({call.task}) assigned to unit {', '.join([worker.call_sign for worker in assigned_worker])}.")
                call.status = "Assigned"
            break
    else:
        print(f"No call found with ID {call_id}.")

#CALL FUNCTIONS END HERE

#WORKER FUNCTIONS BEGIN HERE

#Defines the function to add a new worker
def add_worker():
    call_sign = input("Enter the call sign of the unit: ")
    team = input("Enter the team of the unit: ")
    worker = Worker(call_sign, team)
    workers.append(worker)
    print(f"Unit {call_sign} added.")

#Defines the function to remove a worker
def remove_worker():
    list_workers()
    call_sign = input("Enter the call sign of the unit to remove: ")
    for worker in workers:
        if worker.call_sign == call_sign:
            workers.remove(worker)
            print(f"Unit {call_sign} removed.")
            return
    print(f"No worker found with call sign {call_sign}.")

#Defines the function to list the workers
def list_workers():
    print("Current units:")
    for worker in workers:
        print(f"{worker.call_sign} - Team: {', '.join(worker.team)} - Busy: {worker.busy}")

#WORKER FUNCTIONS END HERE

#ADMIN FUNCTIONS BEGIN HERE

#Allows the user to manually update the amount of workers required
def update_workers_required():
    call_id = int(input("Enter the call ID: "))
    new_teams_required = input("Enter the new teams required for the call (e.g. FIRE-EMS): ")
    for call in calls:
        if call.call_id == call_id:
            old_teams_required = call.teams_required.split("-")
            new_teams_required = new_teams_required.split("-")
            if len(new_teams_required) > len(old_teams_required):
                additional_teams = set(new_teams_required) - set(old_teams_required)
                additional_workers = assign_worker(call, force_match=True, manual_assign=False)
                if not additional_workers:
                    print(f"No available units for additional teams {', '.join(additional_teams)} for call {call.call_id} ({call.task}).")
                    break
                else:
                    call.assigned_worker += additional_workers  # update the assigned_worker attribute of the call
                    assigned_workers = ", ".join([worker.call_sign for worker in call.assigned_worker])
                    print(f"Call {call.call_id} ({call.task}) assigned to additional unit(s) {', '.join([worker.call_sign for worker in additional_workers])}.")
            call.teams_required = "-".join(new_teams_required)
            print(f"Call {call.call_id} ({call.task}) teams required updated to {call.teams_required}.")
            break
    else:
        print("Invalid call ID.")


#ADMIN FUNCTIONS END HERE

#LOGIN AND LOGOUT FUNCTIONS BEGIN HERE

#Defines the function to log out
def logout():
    global calls, workers
    calls = []
    workers = []
    os.system("cls")
    print("You have been logged out. All calls and workers have been wiped.")
    login()

#Defines the function to show the loading screen | This can be disabled
def show_loading():
    print("Loading...")
    for i in range(101):
        time.sleep(0.1)
        print(f"\r{'[' + '#' * i + ' ' * (100-i) + ']'} {i}% complete", end="", flush=True)
    print()

#a list of ranks and their corresponding welcome messages for the login function
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

#Defines the login function
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

#shows the login function
login()

#LOGIN AND LOGOUT FUNCTIONS END HERE

#LOADING SCREEN BEGIN HERE

#shows the ascii art | This can be disabled
time.sleep(3)
print(r"""\
 ____  _  _     _____ ____    ____  _  _____ ___  _   _____ _  ____  _____
/  __\/ \/ \ |\/  __//  __\  /   _\/ \/__ __\\  \//  /    // \/  __\/  __/
|  \/|| || | //|  \  |  \/|  |  /  | |  / \   \  /   |  __\| ||  \/||  \  
|    /| || \// |  /_ |    /  |  \__| |  | |   / /    | |   | ||    /|  /_ 
\_/\_\\_/\__/  \____\\_/\_\  \____/\_/  \_/  /_/     \_/   \_/\_/\_\\____|
                                                                          
 ____  _      ____    ____  _____ ____  ____  _     _____
/  _ \/ \  /|/  _ \  /  __\/  __// ___\/   _\/ \ /\/  __/
| / \|| |\ ||| | \|  |  \/||  \  |    \|  /  | | |||  \  
| |-||| | \||| |_/|  |    /|  /_ \___ ||  \_ | \_/||  /_ 
\_/ \|\_/  \|\____/  \_/\_\\____\\____/\____/\____/\____\                        
    """)
#ASCII ART ABOVE, DO NOT TOUCH
print("Welcome to River City's Fire Department and Emergency Medical Services Management System!")
show_loading()

#LOADING SCREEN END HERE

#MENU FUNCTIONS BEGIN HERE

#Defines the call administration menu
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

#Defines the worker administration menu
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


#Defines the admin menu
def admin_menu():
    while True:
        print("Admin Menu:")
        print("1. Update workers required on call")
        print("Q. Quit Admin Menu")
        choice = input("Enter your choice: ").lower()
        if choice == "1":
            update_workers_required()
        elif choice == "q":
            print("Exiting Admin Menu...")
            break
        else:
            print("Invalid choice.")

#Defines the main menu
def main_menu():
    while True:
        print("Main Menu:")
        print("1. Call Administration")
        print("2. Worker Administration")
        print("3. Admin Menu")
        print("L. Logout")
        print("Q. Quit the program")
        choice = input("Enter your choice: ").lower()
        if choice == "1":
            admin_calls_menu()
        elif choice == "2":
            admin_workers_menu()
        elif choice == "3":
            admin_menu()
            break
        elif choice == "l":
            logout()
        elif choice == "q":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice.")         
print(main_menu())

#MENU FUNCTIONS END HERE