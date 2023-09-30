import socketio


class SocketIOClient:

    def __init__(self, server_url, main_event: str):
        self.server_url = server_url
        self.main_event = main_event
        self.sio = socketio.Client()

        # Define event handlers
        @self.sio.event
        def connect():
            print('Connected to the server via Socket.IO')

        @self.sio.on(self.main_event)
        def handle_message_from_server(data):
            print('Received message from server:', data)

    def connect(self):
        self.sio.connect(self.server_url)

    def send_message_to_server(self, event, message):
        data_to_send = {"message": message}
        self.sio.emit('message_from_client', data_to_send)

    def run(self):
        # Connect to the server and start receiving events
        self.connect()
        self.sio.wait()

    def disconnect(self):
        self.sio.disconnect()
