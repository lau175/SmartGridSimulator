import matlab.engine
from transaction import *




def sortPrice(e):
    return e["price"]


class Negotiation():

    def __init__(self, data_sim):
        # INIT.
        # Data from simulation at each step, one instance of this class for each social circle.
        # Input format: data_sim = [(price, qnt, buy/sell, id), (100, -8, 0, 3), (105, 5, 1, 2), (108, 11, 1, 7)]
        self.data_sim = data_sim
        self.sellers = []
        self.buyers = []
        self.possible = []
        self.not_feasible = []
        self.buy_id = []
        self.sell_id = []
        self.sell_range = []
        self.buy_range = []

        for i in range(len(self.data_sim)):
            if self.data_sim[i][2] == 1: # 1=seller 0=buyer
                self.sellers.append({"id": self.data_sim[i][3], "price": self.data_sim[i][0], "qnt": self.data_sim[i][1]})
            else:
                self.buyers.append({"id": self.data_sim[i][3], "price": self.data_sim[i][0], "qnt": -self.data_sim[i][1]})

        self.sellers.sort(key=sortPrice)
        self.buyers.sort(reverse=True, key=sortPrice)


    def transaction(self):

        # TRANSACTIONS
        while (self.sellers != []) and (self.buyers != []):
            for buyer in self.buyers:
                # Set price as average of the two offers.
                price = (self.sellers[0]["price"] + buyer["price"]) / 2
                # Set quantity to be exchanged based on who needs less.
                if self.sellers[0]["qnt"] >= buyer["qnt"]:
                    qnt = buyer["qnt"]
                    self.sellers[0]["qnt"] -= buyer["qnt"]
                    buyer["qnt"] = 0

                else:
                    qnt = self.sellers[0]["qnt"]
                    buyer["qnt"] -= self.sellers[0]["qnt"]
                    self.sellers[0]["qnt"] = 0

                self.possible.append({"from": self.sellers[0]["id"], "to": buyer["id"], "price": price, "qnt": qnt})

                # If buyer or seller is done, remove it from its respective list.
                if buyer["qnt"] == 0:
                    self.buyers.remove(buyer)

                if self.sellers[0]["qnt"] == 0:
                    self.sellers.pop(0)
                    break


    def feasibility_check(self):
        #MATPOWER CHECK
        #input_list is a list of lists structured like [seller buyer qty]
        #It is the list of possible transactions after the wallet check.
        input_list = []
        if self.possible != []:
            # Due to MATPOWER limitations, id numbers need to be in [2,11]
            for i in self.possible:
                if i["from"] > 11:
                    
                    from_bus= i["from"] % 9 +2
                else:
                    from_bus = i["from"]
                if i["to"] > 11:
                    to_bus= i["to"] % 9 + 2
                else:
                    to_bus = i["to"]
                
                input_list.append([float(from_bus),float(to_bus),float(i["qnt"])])
            
            
            eng = matlab.engine.start_matlab()
            Matpower_res= eng.check(input_list)
        else:
            # If no transactions need to be performed, the MATPOWER check is skipped
            Matpower_res = 1
            

        return self.possible

    def BC_check(self, transactObj, BC_addresses_list, transactions_rx):
        #CHECK WHICH TRANSACTIONS CAN BE DONE ON THE WALLET POINT OF VIEW
        flag = 0
        for each in self.possible:
            buyer=each["to"]
            seller=each["from"]
            amount=each["price"]
            # Perform the check on each proposed transaction.
            SC_res = transactObj.transferFunds(transactions_rx[buyer-2], BC_addresses_list[seller-2], amount)
            if SC_res == False:
                self.possible.remove(each)
                # The following flag was used only for debugging purposes,
                # to see if at least a transaction had failed.
                flag = 1
                
        return flag
            

    def set_prices(self):
        
        # DYNAMIC LEARNING: SET NEW PRICES RANGES
        tot_qnt = 0
        tot_price = 0
        equilibrium_price = 0

        for offert in self.possible:
            tot_qnt += offert['qnt']
            tot_price += offert['price'] * offert['qnt']


        if (tot_qnt != 0) and (tot_price != 0) and (self.possible != []):
            maxPrice = max(self.possible, key=lambda x: x['price'])['price']
            minPrice = min(self.possible, key=lambda x: x['price'])['price']
            equilibrium_price = tot_price / tot_qnt

            if self.buyers != []:
                self.buy_range = (minPrice + 0.1, equilibrium_price)
            if self.sellers != []:
                self.sell_range = (equilibrium_price, maxPrice - 0.1)

            
        return self.buy_range, self.sell_range