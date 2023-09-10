import time
import psutil
import pyautogui
import tkinter as tk
from tkinter import messagebox
import logging

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Define the list of actions to be performed, initially empty
actions = []

def add_action():
    x = x_action_var.get()
    y = y_action_var.get()
    action_type = action_type_var.get()
    
    if action_type == "click":
        actions.append({"coord": (x, y), "action": action_type})
    elif action_type == "scroll":
        value = scroll_value_var.get()
        actions.append({"coord": (x, y), "action": action_type, "value": value})

def add_client():
    x = x_client_var.get()
    y = y_client_var.get()
    name = client_name_var.get()
    clients.append({"coord": (x, y), "name": name})

desired_args = ['C:\\Program Files\\Java\\jre-1.8\\bin\\java.exe', '-jar', 'C:\\Users\\InkoHamza\\.osmb/OSMB.jar', '']
#desired_args=['C:\\Program Files\\Java\\jre-1.8\\bin\\java.exe', '-jar', 'C:\\Users\\Administrator\\.osmb/OSMB.jar', '']

clients = []

# Create a function to run the script
def run_script():
    global clients, actions
    try:
        while True:
            desired_process = None
            for process in psutil.process_iter(attrs=["name", "cmdline", "cpu_percent"]):
                if process.info["name"] == "java.exe" and desired_args == process.info["cmdline"]:
                    logging.info("Found desired Java process.")
                    desired_process = process
                    break

            if desired_process and desired_process.info["cpu_percent"] == 0:
                logging.info(f"Desired Java process with arguments {desired_args} found. Running the script...")

                # Add client positions
                num_clients = len(clients)
                for client in clients:
                    try:
                        pyautogui.moveTo(client["coord"], duration=1)
                        pyautogui.click(client["coord"], duration=1)
                        for action_info in actions:
                            coord = action_info["coord"]
                            action = action_info["action"]
                            pyautogui.moveTo(coord, duration=1)
                            if action == "click":
                                pyautogui.click(coord, duration=1)
                            elif action == "scroll":
                                pyautogui.scroll(action_info["value"])
                        time.sleep(5)

                    except pyautogui.FailSafeException:
                        logging.error("A failsafe exception occurred. Exiting the script.")
                        messagebox.showerror("Error", "A failsafe exception occurred. Exiting the script.")
                        exit()
                    except Exception as e:
                        logging.error(f"An error occurred for client {client['name']}: {e}")
                        messagebox.showerror("Error", f"An error occurred for client {client['name']}: {e}")

                time.sleep(10)
            else:
                time.sleep(10)

    except KeyboardInterrupt:
        logging.info("Script terminated by the user.")
        exit()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
root = tk.Tk()
root.title("Script GUI")

# Create and arrange GUI components
x_action_label = tk.Label(root, text="X Position for Action:")
x_action_var = tk.StringVar()
x_action_entry = tk.Entry(root, textvariable=x_action_var)
y_action_label = tk.Label(root, text="Y Position for Action:")
y_action_var = tk.StringVar()
y_action_entry = tk.Entry(root, textvariable=y_action_var)
action_type_label = tk.Label(root, text="Action Type:")
action_type_var = tk.StringVar(value="click")
action_type_dropdown = tk.OptionMenu(root, action_type_var, "click", "scroll")
scroll_value_label = tk.Label(root, text="Scroll Value:")
scroll_value_var = tk.StringVar()
scroll_value_entry = tk.Entry(root, textvariable=scroll_value_var)

x_client_label = tk.Label(root, text="X Position for Client:")
x_client_var = tk.StringVar()
x_client_entry = tk.Entry(root, textvariable=x_client_var)
y_client_label = tk.Label(root, text="Y Position for Client:")
y_client_var = tk.StringVar()
y_client_entry = tk.Entry(root, textvariable=y_client_var)
client_name_label = tk.Label(root, text="Client Name:")
client_name_var = tk.StringVar()
client_name_entry = tk.Entry(root, textvariable=client_name_var)

add_action_button = tk.Button(root, text="Add Action", command=add_action)
add_client_button = tk.Button(root, text="Add Client", command=add_client)
run_script_button = tk.Button(root, text="Run Script", command=run_script)

# Arrange components using grid layout
x_action_label.grid(row=0, column=0)
x_action_entry.grid(row=0, column=1)
y_action_label.grid(row=1, column=0)
y_action_entry.grid(row=1, column=1)
action_type_label.grid(row=2, column=0)
action_type_dropdown.grid(row=2, column=1)
scroll_value_label.grid(row=3, column=0)
scroll_value_entry.grid(row=3, column=1)

x_client_label.grid(row=4, column=0)
x_client_entry.grid(row=4, column=1)
y_client_label.grid(row=5, column=0)
y_client_entry.grid(row=5, column=1)
client_name_label.grid(row=6, column=0)
client_name_entry.grid(row=6, column=1)

add_action_button.grid(row=7, column=0)
add_client_button.grid(row=7, column=1)
run_script_button.grid(row=8, columnspan=2)

# Start the GUI application
root.mainloop()
