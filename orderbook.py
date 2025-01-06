from os import system, name
import time

class OrderBook:

    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    def __init__(self,orders):
        self.orders = orders
        self.asks = []
        self.bids = []
        for order in self.orders:
            if order.type == 'ask':
                self.asks.append(order)
            if order.type == 'bid':
                self.bids.append(order)
        self.exectuedOrders = []
        self.priceData = []

    def getMidpointPrice(self):
        if len(self.asks) > 0 and len(self.bids) > 0:
            loweastAsk = self.asks[-1]
            highestBid = self.bids[0]
            midpoint = ( loweastAsk.price + highestBid.price ) / 2
        elif len(self.asks) > 0 and len(self.bids) == 0:
            midpoint = self.asks[-1].price
        elif len(self.asks) == 0 and len(self.bids) > 0:
            midpoint = self.bids[0].price
        else:
            midpoint = 0
        return midpoint

    def checkOrders(self):
        """
        Checks if there are any matches between asks and bids
        Uses FIFO for queue processing
        """

        self.asks.sort(key=lambda order: (order.price, order.timeIndex))
        self.bids.sort(key=lambda order: (-order.price, order.timeIndex),)

        for bid in self.bids:

            startTime = time.time()
            prices = []

            for ask in self.asks:
                if ask.price <= bid.price and ask.quantity >= bid.quantity:
                    quantity = bid.quantity
                    ask.quantity -= bid.quantity
                    bid.quantity = 0
                    prices.extend([ask.price] * quantity)
                elif ask.price <= bid.price and ask.quantity < bid.quantity:
                    quantity = ask.quantity
                    bid.quantity -= ask.quantity
                    ask.quantity = 0
                    prices.extend([ask.price] * quantity)

            endTime = time.time()
            if len(prices) > 0:
                avgPrice = sum(prices) / len(prices)
                executionTime = endTime - startTime
                executedOrder = (f'{self.GREEN} === TRADE === {self.RESET}\n'
                                 f'Executed at : {endTime} -> In : {executionTime} seconds\n'
                                 f'{self.BLUE}PRICE: {avgPrice}\n'
                                 f'QUANTITY: {len(prices)}{self.RESET}\n'
                                 f' {self.GREEN}== == == =={self.RESET}')

                self.exectuedOrders.append(executedOrder)
                self.priceData.append((avgPrice,endTime))

        self.asks = [order for order in self.asks if order.quantity != 0]
        self.asks.sort(key=lambda order: (order.price, order.timeIndex),reverse=True)
        self.bids = [order for order in self.bids if order.quantity != 0]

    def display(self):
        """
        prints out asks and bids
        Best used when debugging
        """
        print()
        for order in self.asks:
            print(order.price , order.quantity)
        print('========================')
        for order in self.bids:
            print(order.price , order.quantity)

    def displayPretty(self):
        """
        Writes orderbook to command line with colours and nice formatting
        Also prints orders executed at the top of the page
        (clears previous outputs so can be annoying when debugging)
        """
        cleanedAsks = {}
        for ask in self.asks:
            price = ask.price
            quantity = ask.quantity
            if price in cleanedAsks:
                cleanedAsks[price] += quantity
            else:
                cleanedAsks[price] = quantity

        cleanedBids = {}
        for bid in self.bids:
            price = bid.price
            quantity = bid.quantity
            if price in cleanedBids:
                cleanedBids[price] += quantity
            else:
                cleanedBids[price] = quantity

        clear()
        print()
        for executedOrder in self.exectuedOrders:
            print(executedOrder)
        print('\n \n')
        print(f"{self.BLUE} PRICE     QUANTITY{self.RESET}")

        printLength = 8

        for _ in range(printLength - len(cleanedAsks)):
            print()
        for i, (price, quantity) in enumerate(cleanedAsks.items()):
            if i == 8:
                break
            print(f"{self.RED}{price:.3f}    {quantity}{self.RESET}")

        print(f"\n{self.BLUE}====================={self.RESET}\n")

        for i, (price, quantity) in enumerate(cleanedBids.items()):
            if i == printLength:
                break
            print(f"{self.GREEN}{price:.3f}    {quantity}{self.RESET}")
        for _ in range(printLength - len(cleanedBids)):
            print()


    def addOrder(self,order):
        """
        Adds order to orderbook and checks for matches
        """
        if order.type == 'ask':
            self.asks.append(order)
        if order.type == 'bid':
            self.bids.append(order)
        self.checkOrders()


    def sellLimit(self,order):
        """
        Limit order - sell
        uses FIFO for queue processing
        """
        if len(self.bids) > 0 and self.bids[0].price >= order.price:
            startTime = time.time()
            limitPrice = order.price
            quantity = order.quantity
            prices = []

            for bid in self.bids:
                if bid.price >= limitPrice and bid.quantity >= quantity:
                    prices.extend([bid.price] * quantity)
                    bid.quantity -= quantity
                    quantity = 0
                elif bid.price >= limitPrice and bid.quantity <= quantity:
                    prices.extend([bid.price] * bid.quantity)
                    quantity -= bid.quantity
                    bid.quantity = 0

            avgPrice = sum(prices) / len(prices)
            self.bids = [order for order in self.bids if order.quantity != 0]
            endTime = time.time()
            executionTime = endTime - startTime
            executedOrder = (f'{self.GREEN} === SELL === {self.RESET}\n'
                             f'Executed at : {endTime} -> In : {executionTime} seconds\n'
                             f'{self.BLUE}PRICE: {avgPrice}\n'
                             f'QUANTITY: {order.quantity - quantity}{self.RESET}\n'
                             f' {self.GREEN}== == == =={self.RESET}')
            self.exectuedOrders.append(executedOrder)
            self.priceData.append((avgPrice,endTime))


    def buyLimit(self,order):
        """
        Limit order - buy
        uses FIFO for queue processing
        """
        if len(self.asks) > 0 and self.asks[-1].price <= order.price:
            self.asks.sort(key=lambda order: (order.price, order.timeIndex))
            startTime = time.time()
            limitPrice = order.price
            quantity = order.quantity
            prices = []

            for ask in self.asks:
                if ask.price <= limitPrice and ask.quantity >= quantity:
                    prices.extend([ask.price] * quantity)
                    ask.quantity -= quantity
                    quantity = 0
                elif ask.price <= limitPrice and ask.quantity < quantity:
                    prices.extend([ask.price] * ask.quantity)
                    quantity -= ask.quantity
                    ask.quantity = 0

            avgPrice = sum(prices) / len(prices)
            self.asks = [order for order in self.asks if order.quantity != 0]
            endTime = time.time()
            executionTime = endTime - startTime
            executedOrder = (f'{self.GREEN} === BUY === {self.RESET}\n'
                             f'Executed at : {endTime} -> In : {executionTime} seconds\n'
                             f'{self.BLUE}PRICE: {avgPrice}\n'
                             f'QUANTITY: {order.quantity - quantity}{self.RESET}\n'
                             f' {self.GREEN}== == == =={self.RESET}')
            self.exectuedOrders.append(executedOrder)
            self.priceData.append((avgPrice,endTime))
            self.asks.sort(key=lambda order: (order.price, order.timeIndex),reverse=True)

    def sellMarket(self,order):
        """
        Market order - sell
        uses FIFO for queue processing
        """
        if len(self.bids) > 0:
            startTime = time.time()
            quantity = order.quantity
            prices = []

            for bid in self.bids:
                if bid.quantity <= quantity:
                    prices.extend([bid.price] * bid.quantity)
                    quantity -= bid.quantity
                    bid.quantity = 0
                elif bid.quantity >= quantity:
                    prices.extend([bid.price] * quantity)
                    bid.quantity -= quantity
                    quantity = 0

            avgPrice = sum(prices) / len(prices)
            self.bids = [order for order in self.bids if order.quantity != 0]
            endTime = time.time()
            executionTime = endTime - startTime
            executedOrder = (f'{self.GREEN} === BUY === {self.RESET}\n'
                             f'Executed at : {endTime} -> In : {executionTime} seconds\n'
                             f'{self.BLUE}PRICE: {avgPrice}\n'
                             f'QUANTITY: {order.quantity - quantity}{self.RESET}\n'
                             f' {self.GREEN}== == == =={self.RESET}')
            self.exectuedOrders.append(executedOrder)
            self.priceData.append((avgPrice, endTime))

    def buyMarket(self, order):
        """
        Market order - buy
        uses FIFO for queue processing
        """
        if len(self.asks) > 0:
            self.asks.sort(key=lambda order: (order.price, order.timeIndex))
            startTime = time.time()
            quantity = order.quantity
            prices = []

            for ask in self.asks:
                if ask.quantity <= quantity:
                    prices.extend([ask.price] * ask.quantity)
                    quantity -= ask.quantity
                    ask.quantity = 0
                elif ask.quantity >= quantity:
                    prices.extend([ask.price] * quantity)
                    ask.quantity -= quantity
                    quantity = 0

            avgPrice = sum(prices) / len(prices)
            self.asks = [order for order in self.asks if order.quantity != 0]
            endTime = time.time()
            executionTime = endTime - startTime
            executedOrder = (f'{self.GREEN} === BUY === {self.RESET}\n'
                             f'Executed at : {endTime} -> In : {executionTime} seconds\n'
                             f'{self.BLUE}PRICE: {avgPrice}\n'
                             f'QUANTITY: {order.quantity - quantity}{self.RESET}\n'
                             f' {self.GREEN}== == == =={self.RESET}')
            self.exectuedOrders.append(executedOrder)
            self.priceData.append((avgPrice, endTime))
            self.asks.sort(key=lambda order: (order.price, order.timeIndex),reverse=True)

@staticmethod
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')