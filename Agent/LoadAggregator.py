import pandas as pd
import matlab.engine

#Start MATLAB ENGINE
eng = matlab.engine.start_matlab()


def aggr_by_price(buyers):
        
    aggregated_buyers = {}
    prices_buyers = []

    for i in range(len(buyers)):
        prices_buyers.append(buyers[i][2])
    
    prices_buyers = list(set(prices_buyers))
    quantity = 0
    input_buyers = []
    #Create list of possible fake ids
    aggregated_buyers = {key: list() for key in range(3, len(prices_buyers) + 3)}
    
    for i in range(len(prices_buyers)):
        price = prices_buyers[i]
        id_matlab = i + 3 #id such that the aggregated request is not associated to slack bus or LM bus 
        quantity= 0
        for j in range(len(buyers)):
            if buyers[j][2] == price:
                #Create list for disaggregation phase
                #Register the ids of the prosumers proposing the same price
                aggregated_buyers[id_matlab].append(buyers[j][0])
                #Compute aggregated quantity for each proposed price
                quantity += buyers[j][1]
        #Create input list for matlab function        
        input_buyers.append([float(id_matlab), float(quantity), float(price)])
    
    
    return input_buyers, aggregated_buyers


def from_list_to_df(lista) :  
    
    df = pd.DataFrame(lista, columns=["id", "quantity", "price"])
    
    df = df.set_index('id')
    df = df.astype(float, copy=True, errors='raise')
    
    return df



def disaggregation(df,df2,input_buyers, aggregated_list):

    for b in range(3, len(input_buyers) + 3):
        
        aggregated = aggregated_list[b]

        #For each prosumer id under the same fake id, the power and money
        #quantity exchanged with the LM are regitered
        
        
        for i in aggregated:
            
            
            
            if (input_buyers[b - 3][1] - df2['quantity'][i])>0:
                df['quantity'][i] = df2['quantity'][i]
                
                input_buyers[b - 3][1] -= df2['quantity'][i]
          
            else:
                df['quantity'][i] = input_buyers[b - 3][1]
                input_buyers[b - 3][1] = 0
                 
                
            df['price'][i] = input_buyers[b - 3][2]
            
    return df

def LoadAggregator(buyers, sellers):
    
    print("--------------START BUYER LEC------")
    input_buyers, aggregated_buyers = aggr_by_price(buyers)
  
    #Go to LM only if there are buyers 
    if input_buyers != []:
        LEC_qty_b,LEC_prc_b = eng.LEC4buyers(input_buyers,nargout=2)
        
    else:
        LEC_qty_b = []
        LEC_prc_b = []  
        
    #Save results from MATLAB simulation in DF
    for b in range(len(input_buyers)):
        input_buyers[b][1] = LEC_qty_b[b]
        input_buyers[b][2] = LEC_prc_b[b]
    
    
    df = from_list_to_df(buyers)
    df2 = from_list_to_df(buyers)
    
    #Disaggregation
    df = disaggregation(df, df2, input_buyers, aggregated_buyers)
    
    print("--------------START SELLER LEC------")

    
    
    input_sellers, aggregated_sellers = aggr_by_price(sellers)

    if input_sellers != []:
        
        LEC_qty_s,LEC_prc_s = eng.LEC4sellers(input_sellers,nargout=2)
        #delete first row of results cause related to slack
        LEC_qty_s.pop(0)
        LEC_prc_s.pop(0)
        
    else:
        LEC_qty_s = []
        LEC_prc_s = []
    

    
    for b in range(len(input_sellers)):
        input_sellers[b][1] = LEC_qty_s[b]
        input_sellers[b][2] = LEC_prc_s[b]
    
        
    
    
    dfs = from_list_to_df(sellers)
    dfs2 = from_list_to_df(sellers)
    
    dfs = disaggregation(dfs, dfs2, input_sellers, aggregated_sellers)
    
    return df, dfs



    
    
    
    
    
