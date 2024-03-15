class CarRepository:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self, car_id):
        self.cars = [car for car in self.cars if car.id != car_id]

    def find_car_by_id(self, car_id):
        return next((car for car in self.cars if car.id == car_id), None)

    def get_available_cars(self):
        return [car for car in self.cars if car.is_available]
    
    def get_all_cars(self):
        return [car for car in self.cars]
    
    def update_car(self, updated_car):
        for i, car in enumerate(self.cars):
            if car.id == updated_car.id:
                self.cars[i] = updated_car
                break
    
    def lock_car(self, car_id):
        car = self.find_car_by_id(car_id)
        if car:
            car.is_locked = True

    def unlock_car(self, car_id):
        car = self.find_car_by_id(car_id)
        if car:
            car.is_locked = False
    
