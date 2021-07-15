from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import SmartGrid


   
class BalancedElement(TextElement):
    """
    Display a text count of how many BALANCED agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Balanced agents: green "  #+ str(model.balanced)




'''
class BuyingElement(TextElement):
    """
    Display a text count of how many BUYING agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Buyers: red" #+ str(model.tot_buyers)

class SellingElement(TextElement):
    """
    Display a text count of how many SELLING agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Sellers: blue"# + str(model.tot_sellers)

   
class Warning_(TextElement):
    """
    Display a text count of how many BALANCED agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "2 steps corresponds to 1 hour"

'''


def smartgrid_draw(agent):

    
    #print("iteration", iteration)
    
    if agent is None:
        return
    #portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.activity == "Residential":
        
        portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
        if (agent.type == 0) and (agent.balanced==0):
            portrayal["Color"] = ["#FF0000", "#FF9999"]
            portrayal["stroke_color"] = "#00FF00"
        elif (agent.type == 1) and (agent.balanced==0):
            portrayal["Color"] = ["#0000FF", "#9999FF"]
            portrayal["stroke_color"] = "#000000"
        elif agent.balanced==1:
            portrayal["Color"] = ["#00FF00", "#228B22"]
            portrayal["stroke_color"] = "#000000"
        else:
            portrayal["Color"] = ["#FFFF00", "#FFFFE0"]
            portrayal["stroke_color"] = "#000000"

    elif agent.activity == "Business":
        portrayal = {"Shape": "rect", "w": 0.5, "h": 0.5, "Filled": "true", "Layer": 0}
        if (agent.type == 0) and (agent.balanced==0):
            portrayal["Color"] = ["#FF0000", "#FF9999"]
            portrayal["stroke_color"] = "#00FF00"
        elif (agent.type == 1) and (agent.balanced==0):
            portrayal["Color"] = ["#0000FF", "#9999FF"]
            portrayal["stroke_color"] = "#000000"
        elif agent.balanced==1:
            portrayal["Color"] = ["#00FF00", "#228B22"]
            portrayal["stroke_color"] = "#000000"
        else:
            portrayal["Color"] = ["#FFFF00", "#FFFFE0"]
            portrayal["stroke_color"] = "#000000"
    
    
   # print ("iter", iter)
    return portrayal

#Welcome_Message = Warning_()
#balanced_element = BalancedElement()
#buying_element = BuyingElement()
#selling_element = SellingElement()
canvas_element = CanvasGrid(smartgrid_draw, 20, 20, 500, 500)
balanced_chart = ChartModule([{"Label": "Self balanced", "Color": "Green"}])
#energy_chart = ChartModule([{"Label": "total_energy", "Color": "Black"}])
price_chart = ChartModule([{"Label": "Average price of Bilateral Negotiations - C1", "Color": "Red"}])
price_chart_others1 = ChartModule([{"Label": "Average price of Bilateral Negotiations - C2", "Color": "Red"},{"Label": "Average price of Bilateral Negotiations - C3", "Color": "Green"},{"Label": "Average price of Bilateral Negotiations - C4", "Color": "Blue"}])
price_chart_others2 = ChartModule([{"Label": "Average price of Bilateral Negotiations - C5", "Color": "Red"},{"Label": "Average price of Bilateral Negotiations - C6", "Color": "Green"},{"Label": "Average price of Bilateral Negotiations - C7", "Color": "Blue"}])
price_chart_others3 = ChartModule([{"Label": "Average price of Bilateral Negotiations - C8", "Color": "Red"},{"Label": "Average price of Bilateral Negotiations - C9", "Color": "Green"}])
#price_chart2 = ChartModule([{"Label": "Average price of LM", "Color": "Blue"}])
exchanges_chart1 = ChartModule([{"Label": "Exchanged Power among Prosumers [kW]", "Color": "Red"}])
exchanges_chart2 = ChartModule([{"Label": "Exchanged Power with LM [kW]", "Color": "Blue"}])
residential_chart = ChartModule([{"Label": "Residential Consumption [kW]", "Color": "Red"}, {"Label": "Residential Generation [kW]", "Color": "Blue"}])
business_chart = ChartModule([{"Label": "Business Consumption [kW]", "Color": "Red"}, {"Label": "Business Generation [kW]", "Color": "Blue"}])
balanced= ChartModule([{"Label": "Balanced through Negotiation", "Color": "Red"}, {"Label": "Balanced through LM", "Color": "Blue"}])


model_params = {
    "height": 20,
    "width": 20,
    "minority_pc": UserSettableParameter(
        "slider", "Probability of awareness", 0.2, 0.05, 1.0, 0.05
    ),
    "activity_pc": UserSettableParameter(
        "slider", "Percentage of commercial activities", 0.5, 0.05, 1.0, 0.05),
}

server = ModularServer(
    SmartGrid, [ canvas_element, balanced_chart, balanced, exchanges_chart1, exchanges_chart2, price_chart, price_chart_others1, price_chart_others2, price_chart_others3,  residential_chart, business_chart],
                 "SmartGrid", model_params
)

