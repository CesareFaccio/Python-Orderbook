from order import Order
from orderbook import OrderBook

def main():

    orders = []
    orderbook = OrderBook(orders)

    askPrices = [203,204,202,240,220]
    askVolumes = [30,25,23,32,50]

    for askPrice,askVolume in zip(askPrices, askVolumes):
        orderbook.addOrder(Order('ask', askPrice, askVolume))

    bidPrices = [180, 195, 198, 100, 165]
    bidVolumes = [35, 11, 32, 75, 43]

    for bidPrice,bidVolume in zip(bidPrices, bidVolumes):
        orderbook.addOrder(Order('bid', bidPrice, bidVolume))

    """
    Bellow I add orders to check if trades are executed correctly,
    I use P for price and Q for quantity at which we should se a resulting trade execute
    """
    orderbook.addOrder(Order('bid', 203, 100)) #trade at P:(202,203) Q:53
    orderbook.addOrder(Order('ask', 200, 20)) #trade at P:200 Q:20
    orderbook.addOrder(Order('ask', 225, 30)) #no trade
    orderbook.addOrder(Order('ask', 180, 59)) #trade at P:203 Q:27 and P:198 Q:32

    orderbook.sellLimit(Order('sell', 190, 50)) #trade at P:195 Q:11
    orderbook.buyLimit(Order('buy', 204, 50)) #trade at P:204 Q: 25

    orderbook.buyMarket(Order('buy', 0, 55)) #trade at P:(220,225) Q:55
    orderbook.sellMarket(Order('sell', 0, 40)) #trade at P:(165,180) Q:40

    askPrices = [203, 204, 202, 245, 220]
    askVolumes = [30, 25, 23, 37, 50]

    for askPrice, askVolume in zip(askPrices, askVolumes):
        orderbook.addOrder(Order('ask', askPrice, askVolume))

    bidPrices = [180, 195, 198, 101, 150]
    bidVolumes = [35, 11, 32, 67, 43]

    for bidPrice, bidVolume in zip(bidPrices, bidVolumes):
        orderbook.addOrder(Order('bid', bidPrice, bidVolume))

    """
    Below is what we expect to be printed as the resulting orderbook:
    
            START:                                         END:
    
    
                                               245 37
                                               240 32
    240 32                                     225 25
    220 50                                     220 50
    204 25                                     204 25
    203 30                                     203 30
    202 23                                     202 23
    ========================                   ========================  
    198 32                                     198 32
    195 11                                     195 11
    180 35                                     180 35
    165 43                                     165 38
    100 75                                     150 43
                                               101 67
                                               100 75
               
    """

    orderbook.displayPretty()

if __name__ == '__main__':
    main()