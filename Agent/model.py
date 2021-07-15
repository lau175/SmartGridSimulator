from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

import random
import copy
import json
import numpy as np
import pandas as pd
import time

from smartMeter import *
from transaction import *
from Negotiation import *
from priceStrategy import *
from LoadAggregator import *

class SGAgent(Agent):
    """
    Smart Grid agent
    """

    def __init__(self, unique_id, pos, model, agent_community, activity, transactions_rx=None, BC_address=None):
        """
        Create a new agent.
        Args:
           unique_id: Unique identifier for the agent.
           pos: Agent initial location.
           activity: Indicator for the agent's type business/residential
           agent_community: social circle of the agent
           BC_address: prosumer's address on Ganache
           transactions_rx: receipt after smart contract deployment
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = -1
        self.id = unique_id
        self.neigh = agent_community  # 1=>in "self-balancing" community, 0=> goes directly to LA
        self.balanced = 0
        self.energy = 0
        self.activity = activity
        self.price_buy = np.random.uniform(1, 5)
        self.price_sell = np.random.uniform(1, 5)
        self.price_negotiation = random.randint(1, 10)
        self.transactions_rx = transactions_rx
        self.BC_address = BC_address
        self.balanced_self=0

    def step(self):

        # Noise is added to the average profile, so that for each agent the profile is unique.
        
        # At the beginning of each hour, generation and consumption are computed.
        if self.model.iter % 2 == 0:
            self.balanced_self=0
            
            # Probability to be aware.
            if random.randint(0, 10) < 10 * self.model.minority_pc:
                sign = -1  # not wasteful
            else:
                sign = 1  # wasteful

            # Adding the noise to the average consumption value.
            if self.activity == "Residential":
                noise_cons = random.uniform(0, self.model.consump_r / 10)
                self.cons = self.model.consump_r + (sign * noise_cons)
                self.cons = self.cons
            elif self.activity == "Business":
                noise_cons = random.uniform(0, self.model.consump_b / 10)
                self.cons = self.model.consump_b + (sign * noise_cons)
                self.cons = self.cons

            # Genaration is not affected by awareness, since it depends on natural phenomena (sun/wind)
            self.gen = self.model.gen

            self.energy += (self.gen - self.cons)
            # If the generation and consumprion have (almost) the same value, the agent is self-balanced.
            if self.energy > -0.001 and self.energy < 0.001 and self.model.hour != 0:
                self.balanced_self=1

        
        # The balance check is performed also at the end of each hour, after the transactions.
        if self.energy > -0.001 and self.energy < 0.001 and self.model.hour != 0:
            self.balanced = 1
        else:
            self.balanced = 0
            if self.energy > 0.001:
                self.type = 1  # venditore
            elif self.energy < -0.001:
                self.type = 0  # compratore

        if self.model.iter % 2 == 0:
            
            # If no self-balance, a bid is prepared for the direct negotiations.
            if self.balanced == 0:
                
                # Check the type of the prosumer.
                if self.type == 1:
                    self.price_negotitation = self.price_sell  # monetary unit = ether

                elif self.type == 0:
                    self.price_negotitation = self.price_buy
                
                # Check the social circle of the prosumer.
                # This part can be modified in the future if not all the groups are connected to a Blockchain.
                if self.neigh == 1:
                    self.model.datasim.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 2:
                    self.model.datasim2.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 3:
                    self.model.datasim3.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 4:
                    self.model.datasim4.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 5:
                    self.model.datasim5.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 6:
                    self.model.datasim6.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 7:
                    self.model.datasim7.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 8:
                    self.model.datasim8.append((self.price_negotitation, self.energy, self.type, self.id))
                elif self.neigh == 9:
                    self.model.datasim9.append((self.price_negotitation, self.energy, self.type, self.id))
            
            # We enter this "else" if self.balanced==1.
            else:
                pass



class SmartGrid(Model):
    """
    Model class for the Smart Grid model.
    """

    def __init__(self, height=20, width=20, minority_pc=0.2, activity_pc=0.5):

        # General empty list that will contain all the proposals for negotiations.
        self.datasim = []
        self.datasim2 = []
        self.datasim3 = []
        self.datasim4 = []
        self.datasim5 = []
        self.datasim6 = []
        self.datasim7 = []
        self.datasim8 = []
        self.datasim9 = []

        # Init. negotiation params.
        self.av_price=0
        self.av_price_others=[]
        self.total_qnt=0

        # Grid and simulation params.
        self.height = height
        self.width = width
        self.minority_pc = minority_pc
        self.activity_pc = activity_pc        
        self.iter = 0
        self.hour = 0
        self.buyers = []
        self.sellers = []

        # Blockchain params.
        self.BC_addresses_list = []
        self.transactions_rx = []
        self.negotiation_results = []
        self.transactObj = performTransaction()
        self.BC_addresses_list = self.transactObj.getaddresses(range(0, 81))

        ############### GET ENERGY PROFILE #########################################################
        self.sm = smartMeter()
        solar = self.sm.getSolarProduction(self.hour)
        wind = self.sm.getWindProduction(self.hour)
        self.gen = (solar + wind)
        self.consump_r = 0
        self.consump_b = 0
        self.prc = priceStrategy()
        self.market_price = self.prc.getPrice(self.hour)
        self.buyers_results = pd.DataFrame()
        self.sellers_results = pd.DataFrame()
        #############################################################################################

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.balanced = 0
        self.tot_energy = 0
        
        # At each end of the hour (even steps, i.e. after negotiations),
        # the following data will be collected:
        self.datacollector = DataCollector(

            {"Self balanced": lambda a: a.count_balanced()[0],
             "Balanced through Negotiation": lambda a: a.balanced_by_neg(),
             "Balanced through LM": lambda a: a.count_balanced()[1], 
              "Exchanged Power among Prosumers [kW]": lambda a: a.count_transactions(),
              "Exchanged Power with LM [kW]": lambda a: a.lec_exchanged()[0],
              "Average price of Bilateral Negotiations - C1": lambda a: a.read_scalar(self.av_price),
              "Average price of Bilateral Negotiations - C2": lambda a: a.read_values(self.av_price_others,0),
              "Average price of Bilateral Negotiations - C3": lambda a: a.read_values(self.av_price_others,1),
              "Average price of Bilateral Negotiations - C4": lambda a: a.read_values(self.av_price_others,2),
              "Average price of Bilateral Negotiations - C5": lambda a: a.read_values(self.av_price_others,3),
              "Average price of Bilateral Negotiations - C6": lambda a: a.read_values(self.av_price_others,4),
              "Average price of Bilateral Negotiations - C7": lambda a: a.read_values(self.av_price_others,5),
              "Average price of Bilateral Negotiations - C8": lambda a: a.read_values(self.av_price_others,6),
              "Average price of Bilateral Negotiations - C9": lambda a: a.read_values(self.av_price_others,7),
              "Residential Consumption [kW]": lambda a: a.get_profile()[1],
              "Business Consumption [kW]": lambda a: a.get_profile()[0],
              "Residential Generation [kW]": lambda a: a.get_profile()[2],
              "Business Generation [kW]": lambda a: a.get_profile()[2]
              
              }
        )

        # Set up agents

        # First two id numbers needed by MATPOWER
        new_id = 2
        self.list_agents = []

        # Building the first neighbourhood.
        # This part can be modified if this is thee only group connected to the Blockchain.
        self.community = [(2, 2), (2, 4), (2, 6), (2, 8), (2, 10), (2, 12), (2, 14), (2, 16),
                          (2, 18)]  

        self.transactions_rx = self.transactObj.deploySC(self.BC_addresses_list)

        # FIRST COMMUNITY:
        for cell in self.community:
            x = cell[0]
            y = cell[1]

            agent_community = 1  # Community id

            if random.uniform(0, 1) < self.activity_pc:

                activity = "Business"
                
            else:
                activity = "Residential"

            agent = SGAgent(new_id, (x, y), self, agent_community, activity, self.transactions_rx[new_id - 2],
                            self.BC_addresses_list[new_id - 2])
            self.grid.position_agent(agent, x, y)
            self.list_agents.append(agent)
            self.schedule.add(agent)

            new_id += 1


        # 2-9 COMMUNITIES:
        for i in range(4, 19, 2):
            for j in range(2, 19, 2):

                # TODO: WHY I/2
                agent_community = i / 2  # The agent is part of group n. i/2

                if random.uniform(0, 1) < self.activity_pc:
                    activity = "Business"
                else:
                    activity = "Residential"

                agent = SGAgent(new_id, (i, j), self, agent_community, activity,self.transactions_rx[new_id - 2],
                            self.BC_addresses_list[new_id - 2])
                self.grid.position_agent(agent, i, j)
                self.list_agents.append(agent)
                self.schedule.add(agent)
                new_id += 1


        self.running = True
        
        
        self.datacollector.collect(self)

        print("...LOADING...")


    ###################### USEFUL FUNCTIONS FOR THE DATACOLLECTOR ######################

    # This function returns the list containing the agents.
    def listAgents(self): 
        return self.list_agents
    
    
    # This function reads data from tuples/lists returned by other functions.
    def read_values(self,element, pos=None):
        if element!=[] and element!=None:
            if pos!=None: 
                if len(element)>pos:
                    return element[pos]
                else:
                    return 0
            else:
                return element
        else:
            return 0

    #  This function reads data from tuples/lists returned by other functions.
    def read_scalar(self,element):
        return element

    
    # This method counts the n. of self-balanced agents.
    def count_balanced(self):  

        balanced = 0
        balanced_by_itself=0
        self.tot_buyers = 0
        balanced_by_LM = 0
        self.tot_sellers = 0
        if self.iter == 0: 
            
            return (0,0,0,0)
        
        else:
            
            balanced = 0
            tot_buyers = 0
            tot_sellers = 0
            for agent in self.list_agents:
                if agent.balanced == 1:
                    balanced += 1
                elif agent.type == 1:
                    self.tot_sellers += 1
                elif agent.type == 0:
                    self.tot_buyers += 1

                if agent.balanced_self==1:
                    balanced_by_itself+=1
                
            balanced_by_LM = balanced - (self.balanced_by_negotiation+balanced_by_itself)

            return [balanced_by_itself,balanced_by_LM]


    # this method counts the n. of balanced agents through negotiations.
    def balanced_by_neg(self):
        if self.iter == 0:
            return 0
        else:
            return self.balanced_by_negotiation


    # This method counts the energy exchanged with the local market.
    def lec_exchanged(self ):
        
        tot_pow = 0
        avg_price = 0
        if self.iter == 0: 
            return (0,0)
        else: 
            if not self.buyers_results.empty:
        
                for i in self.buyers_results.index:
                    
                    tot_pow += self.buyers_results["quantity"][i]
                    avg_price += self.buyers_results["price"][i]
        
            if not self.sellers_results.empty:
        
                for j in self.sellers_results.index:
                    #seller = self.list_agents[int(j) - 2]
                    tot_pow += self.sellers_results["quantity"][j]
                    avg_price += self.sellers_results["price"][j]
                    
            if self.buyers_results.shape[0] != 0 or self.sellers_results.shape[0] != 0:
                avg_price /= (self.buyers_results.shape[0] + self.sellers_results.shape[0])

            return (tot_pow, avg_price)


    # This method counts the energy exchanged through direct negotiations.
    def count_transactions(self):
        total_qnt = 0
        self.av_price = 0
        self.av_price_others=[]
        av_price2=0
        i=2

        if self.iter == 0: 
            
            return 0
        
        else:
            for element in self.negotiation_results:
                total_qnt += element['qnt']
                self.av_price += element['price']
            if self.negotiation_results != []:
                self.av_price /= (len(self.negotiation_results))
            for negotiation_result in self.negotiation_results_total:
                i+=1
                av_price2=0
                for element in negotiation_result:
                    total_qnt += element['qnt']
                    av_price2+= element['price']
                if negotiation_result!=[]:
                    self.av_price_others.append(av_price2/len(negotiation_result))
                else:
                    self.av_price_others.append(0)

            return total_qnt
            
            
    # This method gets the profile to show it in the web page.
    def get_profile(self):
        
        if self.iter == 0: 
            
            return (0, 0, 0)
        
        else:
            return (self.consump_b, self.consump_r, self.gen)

    #####################################################################################

    def step(self):

        print("step is ", self.iter)
        
        # Operations to be performed at the beginnig of each hour (even steps).
        if self.iter % 2 == 0:

            # Get consumption and production values.
            solar = self.sm.getSolarProduction(self.hour)
            wind = self.sm.getWindProduction(self.hour)

            self.gen = (solar + wind)
            self.consump_r, self.consump_b = self.sm.getConsumption(self.hour)
            self.market_price = self.prc.getPrice(self.hour)

            self.negotiation_results = []
            self.negotiation_results2 = []
            self.negotiation_results3 = []
            self.negotiation_results4 = []
            self.negotiation_results5 = []
            self.negotiation_results6 = []
            self.negotiation_results7 = []
            self.negotiation_results8 = []
            self.negotiation_results9 = []

            
            # Direct negotiations for the social circles.
            neg = Negotiation(self.datasim)
            neg.transaction()  

            neg2 = Negotiation(self.datasim2)
            neg2.transaction()
            neg3 = Negotiation(self.datasim3)
            neg3.transaction()
            neg4 = Negotiation(self.datasim4)
            neg4.transaction()
            neg5 = Negotiation(self.datasim5)
            neg5.transaction()
            neg6 = Negotiation(self.datasim6)
            neg6.transaction()
            neg7 = Negotiation(self.datasim7)
            neg7.transaction()
            neg8 = Negotiation(self.datasim8)
            neg8.transaction()
            neg9 = Negotiation(self.datasim9)
            neg9.transaction()

            # Check on the wallets (i.e. if the buyers can really afford to pay).
            changed = neg.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed2 = neg2.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed3 = neg3.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed4 = neg4.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed5 = neg5.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed6 = neg6.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed7 = neg7.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed8 = neg8.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            changed9 = neg9.BC_check(self.transactObj, self.BC_addresses_list, self.transactions_rx)
            
            # Check the transaction feasibility with MATPOWER.
            self.negotiation_results = neg.feasibility_check()
            
            self.negotiation_results2 = neg2.feasibility_check()
            self.negotiation_results3 = neg3.feasibility_check()
            self.negotiation_results4 = neg4.feasibility_check()
            self.negotiation_results5 = neg5.feasibility_check()
            self.negotiation_results6 = neg6.feasibility_check()
            self.negotiation_results7 = neg7.feasibility_check()
            self.negotiation_results8 = neg8.feasibility_check()
            self.negotiation_results9 = neg9.feasibility_check()
            
            # For each social circle, agents learn the range of prices that resulted in succesful transactions.

            buy_range=None
            sell_range=None
            buy_range, sell_range = neg.set_prices()
            for agent in self.list_agents[0:9]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C1 ", buy_range, sell_range, "at step: ", self.iter)

            buy_range=None
            sell_range=None
            buy_range, sell_range = neg2.set_prices()
            for agent in self.list_agents[9:18]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C2 ", buy_range, sell_range, "at step: ", self.iter)

            buy_range=None
            sell_range=None
            buy_range, sell_range = neg3.set_prices()
            for agent in self.list_agents[18:27]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C3 ", buy_range, sell_range, "at step: ", self.iter)

            buy_range, sell_range = neg4.set_prices()
            for agent in self.list_agents[27:36]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C4 ", buy_range, sell_range, "at step: ", self.iter)

            buy_range, sell_range = neg5.set_prices()
            for agent in self.list_agents[36:45]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C5 ", buy_range, sell_range, "at step: ", self.iter)

            buy_range, sell_range = neg6.set_prices()
            for agent in self.list_agents[45:54]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C6 ", buy_range, sell_range, "at step: ", self.iter)

            buy_range, sell_range = neg7.set_prices()
            for agent in self.list_agents[63:72]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C7 ", buy_range, sell_range, "at step: ", self.iter)

            buy_range, sell_range = neg8.set_prices()
            for agent in self.list_agents[72:]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C8 ", buy_range, sell_range, "at step: ", self.iter)
            
            buy_range, sell_range = neg9.set_prices()
            #for Id in buy_id:
            for agent in self.list_agents[0:9]:
                if buy_range!=[]:
                    agent.price_buy = random.uniform(buy_range[0], buy_range[1])
                if sell_range!=[]:
                    agent.price_sell = random.uniform(sell_range[0], sell_range[1])

            #print("new price ranges C9 ", buy_range, sell_range, "at step: ", self.iter)

            # Negotiation results.
            self.datasim = []
            self.datasim2 = []
            self.datasim3 = []
            self.datasim4 = []
            self.datasim5 = []
            self.datasim6 = []
            self.datasim7 = []
            self.datasim8 = []
            self.datasim9 = []

            # Check for balance after direct negotiations for group 1.
            self.balanced_by_negotiation = 0 
            for result in self.negotiation_results:
                seller_index = result['from'] - 2
                seller = self.list_agents[seller_index]
                
                seller.energy -= result["qnt"]
                if seller.energy > -0.001 and seller.energy < 0.001:
                    seller.balanced = 1
                    self.balanced_by_negotiation += 1
                else:
                    seller.balanced = 0

                buyer_index = result['to'] - 2
                buyer = self.list_agents[buyer_index]
                buyer.energy += result["qnt"]
                if buyer.energy > -0.001 and buyer.energy < 0.001:
                    buyer.balanced = 1
                    self.balanced_by_negotiation += 1
                else:
                    buyer.balanced = 0
            
            # Check for balance after direct negotiations for groups 2-9.
            self.negotiation_results_total=[]  
            self.negotiation_results_total =[self.negotiation_results2,self.negotiation_results3,self.negotiation_results4,self.negotiation_results5,self.negotiation_results6,self.negotiation_results7,self.negotiation_results8,self.negotiation_results9]

            for negotiation_result in self.negotiation_results_total:
                for result in negotiation_result:
                    seller_index = result['from'] - 2
                    seller = self.list_agents[seller_index]
                    
                    seller.energy -= result["qnt"]
                    if seller.energy > -0.001 and seller.energy < 0.001:
                        seller.balanced = 1
                        self.balanced_by_negotiation += 1
                    else:
                        seller.balanced = 0

                    buyer_index = result['to'] - 2
                    buyer = self.list_agents[buyer_index]
                    buyer.energy += result["qnt"]
                    if buyer.energy > -0.001 and buyer.energy < 0.001:
                        buyer.balanced = 1
                        self.balanced_by_negotiation += 1
                    else:
                        buyer.balanced = 0

################## LOAD AGGREGATOR ############################################################
            for agent in self.list_agents:

                if (agent.balanced == 0):

                    if agent.type == 0:

                        self.buyers.append(
                            [float(agent.id), abs(float(agent.energy)), self.market_price * abs(float(agent.energy))])

                    elif agent.type == 1:
                        self.sellers.append(
                            [float(agent.id), abs(float(agent.energy)), self.market_price * abs(float(agent.energy))])
            #print("LM CALL")
            self.buyers_results, self.sellers_results = LoadAggregator(self.buyers, self.sellers)
################################################################################################

            # Update energy for agents who performed transactions with the local market.
            if not self.buyers_results.empty:

                for i in self.buyers_results.index:
                    buyer = self.list_agents[int(i) - 2]
                    buyer.energy += self.buyers_results["quantity"][i]

            if not self.sellers_results.empty:

                for j in self.sellers_results.index:
                    seller = self.list_agents[int(j) - 2]
                    seller.energy -= self.sellers_results["quantity"][j]

            self.sellers = []
            self.buyers = []

        # Operations to be performed at the end of each hour (odd steps).
        elif (self.iter % 2) != 0:
            
            #print("----------COLLECTING DATA @ ", self.hour)

            # Count the energy exchanged through direct transactions.
            x=self.count_transactions()

            # Collect data.
            self.datacollector.collect(self)
            print("data collected")
            self.hour += 1
        
        # Prepare for next step.  
        time.sleep(3)
        self.iter += 1

        self.schedule.step()
        print("schedule.step concluded")

        # Stopping condtion.
        if self.iter > 47:  # it actually stops 2 iter later (25)
            self.running = False
            print("---------------simulation completed------------")