from constants.command import CommandEnum
from modules.device_connection import DeviceConnection
from socket_app.socket_device import SocketDevice
import threading as th
import time
import tkinter as tk


class Server:
    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 47108

    def __init__(self, connection_type):
        self.device_type = connection_type
        self.devices: list[DeviceConnection] = []
        self.running = True
        self.user_input = None

    def add_device(self, device_id):
        device_conn = self.device_type(device_id)
        self.devices.append(device_conn)

    def send_device_command(self, device_ip):
        pass

    def get_devices_temperature(self):
        temperature_list = []
        for device in self.devices:
            temperature_list.append(
                (device.device_id, device.get_temperature())
            )
        return temperature_list

    def show_command_list(self):
        print(f"Comandos disponíveis: ")
        print(f"(1) Dispositivo 1")
        print(f"(2) Dispositivo 2")
        # for value in CommandEnum
        print(f"Adicionar dispositivo")

    def close_devices(self):
        for device in self.devices:
            device.close()

    def input_reader(self):
        while self.running:
            self.user_input = input()
            print(f"User input {self.user_input}")
            if self.user_input == "Exit":
                self.running = False

    def run(self):
        input_thread = th.Thread(target=self.input_reader)
        input_thread.start()

        # Create the GUI window
        gui_window = tk.Tk()
        gui_window.title("Temperature Readings")
        gui_window.geometry("800x600")

        temperature_label = tk.Label(gui_window, text="Temperature Readings")
        temperature_label.pack()

        temperature_text = tk.Text(gui_window, height=10, width=30)
        temperature_text.pack()

        def show_device_commands():
            temperature_text.delete(1.0, tk.END)
            temperature_text.insert(tk.END, f"Command 1")

        def update_temperatures():
            while self.running:
                temperature_data: list[tuple] = self.get_devices_temperature()
                temperature_text.delete(1.0, tk.END)
                for device, temp in temperature_data:
                    temperature_text.insert(tk.END, f"{device}: {temp:.2f}°C\n")
                time.sleep(1)
        
        show_commands_button = tk.Button(gui_window, text="Show Commands", command=show_device_commands)
        show_commands_button.pack()

        update_thread = th.Thread(target=update_temperatures)
        update_thread.start()

        def on_closing():
            # This function is called when the window is closed
            print("Window is being closed")
            self.running = False
            self.close_devices()
            update_thread.join()
            gui_window.destroy()  # Close the Tkinter window

        # Bind the on_closing function to the window close event
        gui_window.protocol("WM_DELETE_WINDOW", on_closing)
        gui_window.mainloop()

if __name__ == "__main__":
    server = Server(SocketDevice)
    server.run()
