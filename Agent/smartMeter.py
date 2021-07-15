import pandas as pd
import random

# in the 'prosumerProfile.csv' file you can find the mean energy profile of a prosumer
# at each hour of the simulation each prosumer will call the three functions defined in this class and they will obtain
# their power consumption and production in kWs. This value deviates from the mean value with a standard deviation of 0.2.

class smartMeter():

    def __init__(self):
        self.sigma = 0.2 # standard deviation
        self.df = pd.read_csv('prosumerProfile.csv')

    def getConsumption(self,hour):
        mu = self.df['Residential'][hour] # takes from the table the mean value of the consumption at that specific hour
        consumption_residential = random.gauss(mu, self.sigma) # the value of the consumption will be taken as a gaussian random variable
        if consumption_residential <0:
            consumption_residential=mu

        mu = self.df['Business'][hour]
        consumption_business = random.gauss(mu, self.sigma)
        if consumption_business <0:
            consumption_business=mu

        return consumption_residential, consumption_business

    def getSolarProduction(self,hour):
        sigma = self.sigma
        if hour < 4 or hour > 20: # if it's night time the solar production must be 0
            solar = 0
        else:
            mu = self.df['Solar'][hour] # during day time the solar production can be taken from the table as said before
            solar = random.gauss(mu, self.sigma)
            if solar < 0: # it can happen, especially during dawn/sunset (when the mean value of production is low, around 1.5 kW) the variable 'solar' takes negative value
                solar = 0 # in that case it is put to zero
        return solar

    def getWindProduction(self,hour): # the turbines production depends on the velocity of the wind. I assumed that the velocity of the wind is random, with uniform probability
        max = self.df['Wind'][hour] # micro wind turbines can produce maximum 1 kW, so the value reported in the table is the maximum possible production
        wind = random.uniform(0,max) # tha production value is taken at random between 0 and 1 kW
        return wind
    

#plt.plot(df['Unnamed: 8'][:72].values)
#plt.show()