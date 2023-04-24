# Emergency Services Call Management System

This is a Python script for managing emergency services calls. It allows users to add calls, assign units to calls, close calls, and add or remove workers from the system.

## How to use

To run the script, simply execute the `dispatch.py` file. The script will present a command-line interface with the following options:

1.  Call Administration
2.  Worker Administration
3.  Logout
4.  Quit the program

### Adding a call

To add a new call to the system, select option 1 from the call menu. You will be prompted to enter a task abbreviation (e.g. GSE for Gas Station Explosion). The available task abbreviations and their corresponding tasks and teams required are listed in the `task_mapping` dictionary at the beginning of the script and the end of this file.

After entering the task abbreviation, you will be prompted to confirm whether you want to force assign a worker to the call. If you select "y", the system will attempt to assign a unit to the call even if no unit is available with the required team(s). If you select "n", the system will only assign a unit if one is available with the required team(s).

### Closing a call

To close an existing call, select option 2 from the call menu. You will be prompted to enter the ID of the call you want to close. The system will then attempt to assign a unit to each team required for the call. If a unit is not available with a required team, the system will print a message indicating that no worker is available for that team.


### Listing calls

To list all current calls, select option 3 from the call menu. The system will print a list of all calls, including their ID, task, teams required, status, and assigned unit(s) (if any).

### Adding a unit

To add a new unit to the system, select option 1 from the worker menu. You will be prompted to enter the call sign and team of the new unit.

### Removing a unit

To remove an existing unit from the system, select option 2 from the worker menu. You will be prompted to enter the call sign of the unit you want to remove. The system will then remove the worker from the system.

### Exiting the system

To exit the script, select option Q from the main menu.

#### Call types

 - GSE - Gas station explosion
 - BC - Bridge Collapse
 - MVA - Motor Vehicle Accident
 - PC - Plane Crash
 - SW - Strong Winds
 - TC - Tunnel Collapse
 - OS - Oil Spill
 - CS - Chemical Spill
 - BBF - Building-Bush Fire
 - ALI - Arm-Leg Injury
 - SHA - Stroke-Heart Attack
 - SO - Scattered Oil
 - F - Fall
 - R - Revive