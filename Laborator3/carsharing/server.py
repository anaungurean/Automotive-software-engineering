import socket
import threading
import json
from car_service import CarService
from rental_service import RentalService
from authentication_service import AuthenticationService
from car_repository import CarRepository
from user_repository import UserRepository
import time

class Server:
    def __init__(self, host='127.0.0.1', port=12344):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.car_clients = {}
        self.last_heartbeat = {}
        self.user_repository = UserRepository()
        self.car_repository = CarRepository()
        self.authentication_service = AuthenticationService(self.user_repository)
        self.car_service = CarService(self.car_repository, self.user_repository)
        self.rental_service = RentalService(self.car_repository, self.user_repository)

    def start_server(self):
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket):
        while True:
            try:
                self.check_heartbeats()
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                decoded_message = json.loads(message)
                if 'type' in decoded_message and decoded_message['type'] == 'car_connected':
                    car_id = decoded_message['car_id']
                    self.last_heartbeat[car_id] = time.time()
                    self.car_clients[car_id] = client_socket
                if 'type' in decoded_message and decoded_message['type'] == 'heartbeat':
                    self.last_heartbeat[car_id] = time.time()
                if decoded_message.get('type') in ['car_connected', 'heartbeat']:
                    self.process_car_message(decoded_message, client_socket)
                else:
                    response_message = self.process_message(decoded_message)
                    client_socket.sendall(json.dumps(response_message).encode('utf-8'))
            except Exception as e:
                print(f"Error handling client message: {e}")
                break

    def process_car_message(self, message, client_socket):
        car_id = message.get('car_id')
        msg_type = message.get('type')

        if msg_type == 'car_connected':
            print(f"Car {car_id} connected.")
            response = {"type": "ack", "message": "Car connected successfully"}
            client_socket.sendall(json.dumps(response).encode('utf-8'))

        elif msg_type == 'heartbeat':
            print(f"Heartbeat received from Car {car_id}")
            response = {"type": "success", "message": "Heartbeat sent to server"}
            client_socket.sendall(json.dumps(response).encode('utf-8'))
            
        elif msg_type == 'start_rental':
            print(f"Started rental for {car_id}.")
            response = {"type": "success", "message": "Car started rent successfully"}
            
        elif msg_type == 'end_rental':
            print(f"Ended rental for {car_id}.")
            response = {"type": "success", "message": "Car ended rent successfully"}

        elif msg_type in ['lock_car', 'unlock_car']:
            print(f"Command {msg_type} received for Car {car_id}")

    def is_car_connected(self, car_id):
        return car_id in self.car_clients

    def check_heartbeats(self):
        current_time = time.time()
        for car_id in list(self.last_heartbeat.keys()):
            if current_time - self.last_heartbeat[car_id] > 5:
                print(f"Car {car_id} is considered disconnected.")
                self.car_clients.pop(car_id, None)
                self.last_heartbeat.pop(car_id, None)

    def process_message(self, message):
        try:
            if message['type'] == 'register':
                user_type = message['data']['type']
                name = message['data']['name']
                username = message['data']['username']
                password = message['data']['password']
            
                if user_type in ['owner', 'renter']:
                    success, message = self.authentication_service.register(user_type=user_type, name=name, username=username, password=password)
                    return {"success": success, "message": message}
                else:
                    return {"success": False, "message": "Invalid user type"}

            elif message['type'] == 'login':
                username = message['data']['username']
                password = message['data']['password']
                user, user_type = self.authentication_service.login(username=username, password=password)
                if user:
                    return {"success": True, "message": "Register success!", "user_type": user_type, "id" : user.id}
                else:
                    return {"success": False, "message": "Register failed!"}

            elif message['type'] == 'add_car':
                id = message['data']['id']
                if not self.is_car_connected(id):
                    return {"success": False, "message": "Car is not connected."}
                brand = message['data']['brand']
                model = message['data']['model']
                year = message['data']['year']
                owner_id = message['data']['owner_id']
                success, message = self.car_service.add_car_to_owner(id, brand, model, year, owner_id)
                return {"success": success, "message": message}
            
            elif message['type'] == 'remove_car':
                owner_id = message['data']['owner_id']
                car_id = message['data']['car_id']
                success, msg = self.car_service.remove_car_from_owner(car_id, owner_id)
                return {"success": success, "message": msg}
            
            elif message['type'] == 'view_cars':
                print(self.car_clients)
                owner_id = message['data']['owner_id']
                cars = self.car_service.get_cars_by_owner_id(owner_id)
                connected_cars = [car for car in cars if car.id in self.car_clients]
                if connected_cars:
                    cars_data = [{"id": car.id, "brand": car.brand, "model": car.model, "year": car.year} for car in connected_cars]
                    return {"success": True, "cars": cars_data}
                else:
                    return {"success": False, "message": "No cars found."}
            
            elif message['type'] == 'view_available_cars':
                cars = self.rental_service.get_available_cars()
                connected_cars = [car for car in cars if car.id in self.car_clients]
                if connected_cars:
                    cars_data = [{"id": car.id, "brand": car.brand, "model": car.model, "year": car.year} for car in connected_cars]
                    return {"success": True, "cars": cars_data}
                else:
                    return {"success": False, "message": "No available cars found."}

            elif message['type'] == 'start_rental':
                renter_id = message['data']['renter_id']
                car_id = message['data']['car_id']
                if car_id in self.car_clients:
                    self.car_clients[car_id].sendall(json.dumps({"type": "start_rental", "car_id": car_id}).encode('utf-8'))
                    print(f"Sent start_rental command to car {car_id}.")
                else:
                    print(f"Car {car_id} is not connected.")
                success, msg = self.rental_service.start_rental(renter_id, car_id)
                return {"success": success, "message": msg}
                
            elif message['type'] == 'end_rental':
                renter_id = message['data']['renter_id']
                car_id = message['data']['car_id']
                if car_id in self.car_clients:
                    self.car_clients[car_id].sendall(json.dumps({"type": "end_rental", "car_id": car_id}).encode('utf-8'))
                    print(f"Sent end_rental command to car {car_id}.")
                else:
                    print(f"Car {car_id} is not connected.")
                success, msg = self.rental_service.end_rental(renter_id, car_id)
                return {"success": success, "message": msg}

            else:
                return {"success": False, "message": "random message type"}

        except KeyError as e:
            return {"success": False, "message": f"Key Error: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}


if __name__ == "__main__":
    server = Server()
    server.start_server()
