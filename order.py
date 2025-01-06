import time

class Order:
    def __init__(self, type, price, quantity):
        self.type = type
        self.price = price
        self.quantity = quantity
        self.timeIndex = time.time()
        self.PQT = (price, quantity, self.timeIndex)

    def display(self):
        print(f'Order number: {self.timeIndex}')
        print(f'TYPE : {self.type}')
        print(f'PRICE : {self.price}')
        print(f'QUANTITY : {self.quantity}')
