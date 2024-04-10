import socket
import json
import threading
import time
import uuid

class CarClient:
    def __init__(self, host='127.0.0.1', port=12344):
        self.host = host
        self.port = port
        self.car_id = str(uuid.uuid4())
        self.socket = None

    def connect_to_server(self):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.socket.connect((self.host, self.port))
                print(f"Connected to server. Car ID: {self.car_id}")
                self.send_message({"type": "car_connected", "car_id": self.car_id})
                threading.Thread(target=self.listen_to_server, daemon=True).start()
                threading.Thread(target=self.send_heartbeat, daemon=True).start()
            except Exception as e:
                print(f"Error connecting to server: {e}")
                self.socket = None
        else:
            print("Connection already established.")

    def listen_to_server(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received message: {message}")
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def send_message(self, message):
        if self.socket is not None:
            try:
                self.socket.sendall(json.dumps(message).encode('utf-8'))
            except Exception as e:
                print(f"Error sending message: {e}")

    def send_heartbeat(self):
        while True:
            if self.socket is not None:
                try:
                    self.send_message({"type": "heartbeat", "car_id": self.car_id})
                    time.sleep(3)
                except Exception as e:
                    print(f"Error sending heartbeat: {e}")
                    break

    def close_connection(self):
        if self.socket is not None:
            try:
                self.socket.close()
                print("Connection closed.")
            except Exception as e:
                print(f"Error closing connection: {e}")
            finally:
                self.socket = None

if __name__ == "__main__":
    car_client = CarClient()
    car_client.connect_to_server()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        car_client.close_connection()
