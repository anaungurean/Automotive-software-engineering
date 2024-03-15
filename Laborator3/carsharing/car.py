import uuid

class Car:
    def __init__(self, id, owner_id, brand, model, year, is_available=True, is_locked=True):
        self.id = id
        self.owner_id = owner_id
        self.brand = brand
        self.model = model
        self.year = year
        self.is_available = is_available
        self.is_locked = is_locked
