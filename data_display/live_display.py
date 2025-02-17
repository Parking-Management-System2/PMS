import tkinter as tk
from tkinter import ttk
import threading
import time
from redis_db.car_data import CarData
from redis_db.parking_gate_data import ParkingGateData

class LiveDisplayApp:
    def __init__(self, root, car_data, parking_gate_data):
        self.root = root
        self.car_data = car_data
        self.parking_gate_data = parking_gate_data

        self.root.title("Parking System Live Display")
        self.root.geometry("800x600")

        self.car_tree = ttk.Treeview(self.root, columns=("Registration", "Status", "Position"), show="headings")
        self.car_tree.heading("Registration", text="Registration Number")
        self.car_tree.heading("Status", text="Status")
        self.car_tree.heading("Position", text="Position")
        self.car_tree.pack(fill=tk.BOTH, expand=True)

        self.gate_status_label = tk.Label(self.root, text="Gate Status: Entry - Closed, Exit - Open", font=("Arial", 16))
        self.gate_status_label.pack(pady=20)

        self.update_interval = 1000 # Update every 2 seconds
        self.update_display()

    def update_display(self):
        # Update car data
        self.car_tree.delete(*self.car_tree.get_children())
        cars = self.car_data.get_all_cars()
        for car in cars:
            print(car)
            position = f"({car.get(b'position_upper_x', 'N/A').decode()}, {car.get(b'position_upper_y', 'N/A').decode()})"
            self.car_tree.insert("", "end", values=(car['registration_number'], car.get(b'status', 'N/A'), position))

        # Update gate status
        entry_gate_status = self.parking_gate_data.get_gate_status(0)
        exit_gate_status = self.parking_gate_data.get_gate_status(1)
        self.gate_status_label.config(text=f"Gate Status: Entry - {entry_gate_status.decode()}, Exit - {exit_gate_status.decode()}")

        # Schedule the next update
        self.root.after(self.update_interval, self.update_display)

def start_live_display(car_data, parking_gate_data):
    root = tk.Tk()
    app = LiveDisplayApp(root, car_data, parking_gate_data)
    root.mainloop()