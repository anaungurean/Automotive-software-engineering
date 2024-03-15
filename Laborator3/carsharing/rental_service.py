from car_repository import CarRepository
from user_repository import UserRepository
from user import Renter

class RentalService:
    def __init__(self, car_repository: CarRepository, user_repository: UserRepository):
        self.car_repository = car_repository
        self.user_repository = user_repository

    def start_rental(self, renter_id, car_id):
        renter = self.user_repository.find_user_by_id(renter_id)
        car = self.car_repository.find_car_by_id(car_id)

        if not renter or not isinstance(renter, Renter) or not car or not car.is_available:
            return False, "Rental cannot be started due to invalid input or car availability."

        renter.current_rented_car_id = car_id
        car.is_available = False
        self.car_repository.update_car(car)
        return True, "Rental started successfully."

    def end_rental(self, renter_id, car_id):
        renter = self.user_repository.find_user_by_id(renter_id)
        car = self.car_repository.find_car_by_id(car_id)

        if not renter or not isinstance(renter, Renter) or renter.current_rented_car_id != car_id:
            return False, "Rental cannot be ended due to invalid renter or car ID."

        renter.current_rented_car_id = None
        car.is_available = True
        self.car_repository.update_car(car)
        return True, "Rental ended successfully."
    
    def get_available_cars(self):
        return self.car_repository.get_available_cars()
