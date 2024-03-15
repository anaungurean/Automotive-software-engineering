import uuid

class User:
    def __init__(self, username, password, name):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.name = name

class Owner(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, name)
        self.car_ids = []

    def add_car(self, car_id):
        if car_id not in self.car_ids:
            self.car_ids.append(car_id)

    def remove_car(self, car_id):
        if car_id in self.car_ids:
            self.car_ids.remove(car_id)

class Renter(User):
    def __init__(self, username, password, name):
        super().__init__(username, password, name)
        self.current_rented_car_id = None
        self.has_active_rental = False

    def rent_car(self, car_id):
        if not self.has_active_rental:
            self.current_rented_car_id = car_id
            self.has_active_rental = True

    def return_car(self):
        self.current_rented_car_id = None
        self.has_active_rental = False
