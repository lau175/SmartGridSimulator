import pandas as pd
import random

# in the 'prosumerProfile.csv' file you can find the mean energy profile of a prosumer
# at each hour of the simulation each prosumer will call the three functions defined in this class and they will obtain
# their power consumption and production in kWs. This value deviates from the mean value with a standard deviation of 0.2.

class priceStrategy():

    def __init__(self):
        self.sigma = 1 # standard deviation
        self.df = pd.read_csv('pricesProfile.csv')

    def getPrice(self, hour):
        price = self.df['Price'][hour]
        return price