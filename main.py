from typing import List  
from dataclasses import dataclass  


@dataclass
class Order(object):   
    CreatorID: int   
    Side: bool  
    Quantity: int   
    Price: int  



@dataclass  
class Match(object):   
    Bid: Order   
    Offer: Order     



class Market(object):
    def __init__(self):
        self.Bids: List[Order] = []
        self.Offers: List[Order] = []
        self.Matches: List[Match] = []

    def AddOrder(self, order: Order):
        if order.Side:
            self.Offers.append(order)
        else:
            self.Bids.append(order)

    def MatchOrders(self):   
        self.Bids = sorted(self.Bids, key=lambda x: x.Price)[::-1]
        self.Offers = sorted(self.Offers, key=lambda x: x.Price)

        while (len(self.Bids) > 0 and len(self.Offers) > 0):
            if self.Bids[0].Price < self.Offers[0].Price:
                break
            else:  # self.Bids[0].Price >= self.Offers[0].Price:
                currBid = self.Bids.pop()
                currOffer = self.Offers.pop()
                if currBid.Quantity != currOffer.Quantity:
                    if currBid.Quantity > currOffer.Quantity:
                        newBid = Order(currBid.CreatorID, currBid.Side, currBid.Quantity - currOffer.Quantity, currBid.Price)
                        self.Bids.insert(0, newBid)
                        currBid.Quantity = currOffer.Quantity
                    else:
                        newOffer = Order(currOffer.CreatorID, currOffer.Side, currOffer.Quantity - currBid.Quantity, currOffer.Price)
                        self.Offers.insert(0, newOffer)
                        currOffer.Quantity = currBid.Quantity    
                self.Matches.append(Match(currBid, currOffer))

    def ComputeClearingPrice(self) -> int:   
        if len(self.Matches) == 0:   
            return 0   
        
        clearingPrice = 0   
        cumulativeQuantity = 0
        for match in self.Matches:
            cumulativeQuantity += match.Bid.Quantity
            clearingPrice += match.Bid.Quantity * (match.Bid.Price + match.Offer.Price) / 2
        
        return int(clearingPrice / cumulativeQuantity)





