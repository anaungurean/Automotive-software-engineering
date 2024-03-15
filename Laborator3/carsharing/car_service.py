from car_repository import CarRepository
from user_repository import UserRepository
from user import Owner
from car import Car

class CarService:
    def __init__(self, car_repository: CarRepository, user_repository: UserRepository):
        self.car_repository = car_repository
        self.user_repository = user_repository

    def get_all_cars(self):
        self.car_repository.get_all_cars()

    def add_car_to_owner(self, id, brand, model, year, owner_id):
        owner = self.user_repository.find_user_by_id(owner_id)
        if owner and isinstance(owner, Owner):
            car = Car(id, owner_id, brand, model, year, True, True)
            self.car_repository.add_car(car)
            owner.add_car(car.id)
            return True, "Car add success!"
        return False, "Car add failed!"

    def remove_car_from_owner(self, car_id, owner_id):
        car = self.car_repository.find_car_by_id(car_id)
        owner = self.user_repository.find_user_by_id(owner_id)
        if car and owner and car_id in owner.car_ids:
            self.car_repository.remove_car(car_id)
            owner.remove_car(car_id)
            return True, "Car remove success!"
        return False, "Car remove failed!"

    def get_cars_by_owner_id(self, owner_id):
        return [car for car in self.car_repository.cars if car.owner_id == owner_id]
    
    def lock_car(self, car_id):
        self.car_repository.lock_car(car_id)
    
    def unlock_car(self, car_id):
        self.car_repository.unlock_car(car_id)
    
