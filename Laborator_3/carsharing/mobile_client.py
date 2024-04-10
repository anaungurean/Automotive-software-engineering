import socket
import json

class MobileClient:
    def __init__(self, host='127.0.0.1', port=12344):
        self.host = host
        self.port = port
        self.logged_in_user = None

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(json.dumps(message).encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            decoded_response = json.loads(response)
            print(f"Decoded response: {decoded_response}")
            return decoded_response


    def display_menu(self):
        #os.system('cls')
        if self.logged_in_user:
            print(f"Welcome, {self.logged_in_user['username']}! ({self.logged_in_user['user_type'].capitalize()})")
            if self.logged_in_user['user_type'] == 'renter':
                print("Available options:")
                print("1. View available cars")
                print("2. Rent a car")
                print("3. Return a car")
                print("4. Logout")
            elif self.logged_in_user['user_type'] == 'owner':
                print("Available options:")
                print("1. Register a car")
                print("2. Remove a car")
                print("3. View my cars")
                print("4. Logout")
        else:
            print("Available options:")
            print("1. Login")
            print("2. Register")


    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        response = self.send_message({"type": "login", "data": {"username": username, "password": password}})
        if response['success']:
            self.logged_in_user = {"username": username, "user_type": response['user_type'], "id" : response['id']}
            print("Login success!")
        else:
            print("Login failed!")

    def register(self):
        type = input("Type(owner, renter):")
        name = input("Full Name: ")
        username = input("Username: ")
        password = input("Password: ")
        response = self.send_message({"type": "register", "data": {"type" : type, "name" : name, "username": username, "password": password}})
        if response['success']:
            print("Register success!")
        else:
            print("Register failed!")
    
    def register_car(self):
        print("Register a new car:")
        id = input("Car id: ")
        brand = input("Car brand: ")
        model = input("Car model: ")
        year = input("Year of manufacture: ") 
        
        response = self.send_message({
            "type": "add_car",
            "data": {
                "id" : id,
                "brand": brand,
                "model": model,
                "year": year,
                "owner_id" : self.logged_in_user['id']
            }
        })

    def view_cars(self):
        print("Viewing my cars:")
        response = self.send_message({
            "type": "view_cars",
            "data": {
                "owner_id": self.logged_in_user['id']
            }
        })
        if response['success']:
            print("Your cars:")
            for car in response['cars']:
                print(f"{car['brand']} {car['model']} ({car['year']}) - {car['id']}")
        else:
            print(response['message'])
        
            print(response['message'])

    def remove_car(self):
        print("Remove a car:")
        car_id = input("Enter the car ID to remove: ")
        
        response = self.send_message({
            "type": "remove_car",
            "data": {
                "owner_id": self.logged_in_user['id'],
                "car_id": car_id
            }
        })
        
        print(response['message'])


    def rent_car(self):
        car_id = input("Enter the ID of the car you want to rent: ")
        response = self.send_message({
            "type": "start_rental",
            "data": {
                "renter_id": self.logged_in_user['id'],
                "car_id": car_id
            }
        })
        print(response['message'])

    def return_car(self):
        car_id = input("Enter the ID of the car you are returning: ")
        response = self.send_message({
            "type": "end_rental",
            "data": {
                "renter_id": self.logged_in_user['id'],
                "car_id": car_id
            }
        })
        print(response['message'])

    def view_available_cars(self):
        print("Viewing available cars:")
        response = self.send_message({
            "type": "view_available_cars",
            "data": {}
        })
        if response['success']:
            print("Available cars:")
            for car in response['cars']:
                print(f"{car['id']}: {car['brand']} {car['model']} ({car['year']})")
        else:
            print(response['message'])

    def lock_car(self, car_id):
        self.send_message({"type": "lock_car", "data": {"car_id": car_id}})

    def unlock_car(self, car_id):
        self.send_message({"type": "unlock_car", "data": {"car_id": car_id}})

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choose an option: ").strip()
            if not self.logged_in_user:
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register()
            elif self.logged_in_user['user_type'] == 'renter':
                if choice == "1":
                    self.view_available_cars()
                elif choice == "2":
                    self.rent_car()
                elif choice == "3":
                    self.return_car()
                elif choice == "4":
                    self.logged_in_user = None
                    print("You have logged out.")
            elif self.logged_in_user['user_type'] == 'owner':
                if choice == "1":
                    self.register_car()
                elif choice == "2":
                    self.remove_car()
                elif choice == "3":
                    self.view_cars()
                elif choice == "4":
                    self.logged_in_user = None
                    print("You have logged out.")
            else:
                print("Invalid option.")


if __name__ == "__main__":
    client = MobileClient()
    client.run()
