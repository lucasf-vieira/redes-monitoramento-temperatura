from constants.command import CommandEnum
from modules.device_connection import DeviceConnection
from socket_app.socket_device import SocketDevice
from mqtt_app.mqtt_device import MQTTDevice
from http_app.http_device import HTTPDevice
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
        self.COMMAND_USAGE = {
            "setup": "setup [INDEX DISPOSITIVO] [IP SERVIDOR] [PORTA SERVIDOR]",
            "set_x": "set_x [INDEX DISPOSITIVO] [SEGUNDOS]",
            "set_y": "set_y [INDEX DISPOSITIVO] [SEGUNDOS]",
            "reset": "reset [INDEX DISPOSITIVO]",
            "add":   "add [ID DISPOSITIVO]",
            "ls":    "ls",
        }

    def add_device(self, device_id):
        try:
            print(f"Adding device {device_id}...")
            device_conn = self.device_type(device_id)
            self.devices.append(device_conn)
            print(f"Successfully connected to device")
        except Exception as exc:
            import traceback as tb
            tb.print_exc()
            print(f"Ignoring device {device_id}: {exc}")

    def send_device_command(self, device: DeviceConnection, command, value):
        try:
            device.send_command(command, value)
        except Exception:
            import traceback as tb
            tb.print_exc()
            print(f"Não foi possível enviar comando {command} para o dispositivo {device.device_id}")

    def get_devices_temperature(self):
        temperature_list = []
        for device in self.devices:
            temperature_list.append(
                (device.device_id, device.get_temperature())
            )
        return temperature_list

    def list_devices(self):
        if not self.devices:
            print("Nenhum dispositivo conectado.")
            return
        for index, device in enumerate(self.devices):
            print(f"({index}) Dispositivo {device.device_id}")

    def show_command_list(self):
        print(f"Comandos disponíveis: ")
        SERVER_CMD_DESCRIPTIONS = {
            "help": "Mostra esta lista de comandos",
            "ls": "Lista os dispositivos por index conectados no servidor",
            "setup": "Configura o servidor para o qual o dispositivo envia sua temperatura",
            "set_x": "Define o intervalo em segundos de envio da temperatura do dispositivo para o servidor",
            "set_y": "Define o intervalo em segundos para o dispositivo ler sua temperatura",
            "reset": "Limpa a lista de temperaturas no dispositivo",
            "add": "Adiciona um novo dispositivo no servidor",
        }
        for key in SERVER_CMD_DESCRIPTIONS:
            print(f"    {key}: {SERVER_CMD_DESCRIPTIONS[key]}")

    def do_command(self, user_input: str):
        user_command = user_input.split()
        command = user_command[0]
        if command not in self.COMMAND_USAGE.keys():
            print(f"Comando '{user_input}' não encontrado.")
            return
        if command == "add":
            self.add_device(user_command[1])
            return
        device_index = int(user_command[1])
        if device_index < 0 or device_index > len(self.devices):
            print(f"Index de dispositivo '{device_index}' inválido")
            return
        device = self.devices[device_index]
        if command == CommandEnum.SETUP.value:
            self.send_device_command(
                device,
                command,
                {
                    "server_ip": user_command[2],
                    "server_port": user_command[3]
                }
            )
        if command == CommandEnum.RESET.value:
            self.send_device_command(device, command, "")
        if command in (CommandEnum.SET_X.value, CommandEnum.SET_Y.value):
            self.send_device_command(device, command, user_command[2])

    def _close_devices(self):
        for device in self.devices:
            device.close()

    def run_server(self):
        self.show_command_list()
        while self.running:
            user_input = input()
            if user_input == "" or not self.running:
                continue
            if user_input == "help":
                self.show_command_list()
                continue
            if user_input == "ls":
                self.list_devices()
                continue
            try:
                self.do_command(user_input)
            except Exception as exc:
                print(f"Comando inválido: {exc}")
                print(f"Uso do comando: {self.COMMAND_USAGE[user_input.split()[0]]}")

    def run(self):
        server_thread = th.Thread(target=self.run_server)
        server_thread.start()

        window = self._prepare_gui()
        window.mainloop()

    def _prepare_gui(self):
        def exit():
            # This function is called when the window is closed
            self.running = False
            self._close_devices()
            update_thread.join()
            gui_window.destroy()  # Close the Tkinter window
            print("Pressione a tecla Enter para fechar o servidor")

        def update_temperatures():
            while self.running:
                temperature_data: list[tuple] = self.get_devices_temperature()
                temperature_list.delete(1.0, tk.END)
                for device, temp in temperature_data:
                    if not isinstance(temp, float):
                        continue
                    temperature_list.insert(tk.END, f"{device}: {temp:.2f}°C\n")
                time.sleep(0.05)

        # Create the GUI window
        gui_window = tk.Tk()
        gui_window.title("Temperatura dos Dispositivos")
        gui_window.geometry("400x250")

        temperature_label = tk.Label(gui_window, text="Leituras de Temperatura")
        temperature_label.pack()

        temperature_list = tk.Text(gui_window, height=10, width=40)
        temperature_list.pack()

        update_thread = th.Thread(target=update_temperatures)
        update_thread.start()

        advice_label = tk.Label(
            gui_window,
            text="Utilize o terminal para enviar comandos aos dispositivos",
            pady=10
        )
        advice_label.pack()

        # Bind the on_closing function to the window close event
        gui_window.protocol("WM_DELETE_WINDOW", exit)
        return gui_window


if __name__ == "__main__":
    server = Server(HTTPDevice)
    # server.add_device("127.0.0.1")
    server.run()
