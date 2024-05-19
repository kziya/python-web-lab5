# Create your models here.
class User:
    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email


class Food:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price


class Order:
    def __init__(self, id: int, idUser: int, idFood: int, quantity: int):
        self.id = id
        self.idUser = idUser
        self.idFood = idFood
        self.quantity = quantity
