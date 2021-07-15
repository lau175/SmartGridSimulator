from smartMeter import *
import matplotlib.pyplot as plt

consumption_r = []
consumption_b = []
solar = []
wind = []

for h in range (24):
    sm = smartMeter()

    r,b = sm.getConsumption(h)
    consumption_r.append(r)
    consumption_b.append(b)

    s = sm.getSolarProduction(h)
    solar.append(s)

    w = sm.getWindProduction(h)
    wind.append(w)

plt.grid()
plt.plot(consumption_r)
plt.plot(consumption_b)
plt.plot(solar)
plt.plot(wind)
plt.legend(["Residential","Business","PV panels","Wind turbines"])
plt.title("Energy profile of a prosumer")
plt.ylabel("Power [kW]")
plt.xlabel("Time [h]")
plt.show()



