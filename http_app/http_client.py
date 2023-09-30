from client import Client
import time
import requests


class HTTPClient(Client):
    def __init__(self):
        super().__init__()
    
    def _read(self) -> str:
        try:
            response = requests.get(f"http//{self.server_ip}:{self.server_port}/read_temperature")
            if response.status_code = 200:
                return response.text
            else:
                return""
        except Exception as e:
            print(f"Failed to read data: {str(e)}")
            return ""
        
    def _send(self, average_temperature) -> None:
        try:
            response = requests.post(f"http://{self.server_ip}:{self.server_port}/send_temperature", json={"temperature": average_temperature})
            if response.status_code == 200:
                print(f"Temperature sent to server: {average_temperature}")
            else:
                print(f"Failed to send temperature. Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to send temperature: {str(e)}")



if __name__ == "__main__":
    client = Client()
    client.setup("127.0.0.1", 0808)  # Configure o IP e a porta do servidor
    client.run()
