from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random
import pandas as pd

# helperfunction for recommend
def similarity(x, y, df):
    """
    Gets business x, y, and a dataframe
    Returns similarity between business x and y
    """
   
    categories_x = set()
    categories_y = set()

    # get categories for business x and y
    for number in df.index:
        if x == df.loc[number]['business_id']:
            categories_x = {item.strip() for item in df.loc[number]['categories'].split(',')}
        if y == df.loc[number]['business_id']:
            categories_y = {item.strip() for item in df.loc[number]['categories'].split(',')}
    
    # return 0.0 if there aren't any categories
    if  max(len(categories_x), len(categories_y)) == 0:
        return 0.0
    
    # return similarity between x and y
    return len(categories_x & categories_y) / max(len(categories_x), len(categories_y))


def recommend(business_id, city=None, n=10):
    """
    Returns n recommendations as a list of dicts.
    Takes in a business_id
    Optionally takes in a city.
    A recommendation is a dictionary in the form of:
        {
            business_id:str
            stars:str
            name:str
            city:str
            address:str
        }
    """
    
    # choose random city if no city is given
    if not city:
        city = random.choice(CITIES)
              
    # create dataframe with businesses 
    df = pd.DataFrame(BUSINESSES[city])
        
    similarities = dict()
    
    # calculate similarities
    for item in df.index:
        if not business_id == df.loc[item]['business_id']:
            similarities[df.loc[item]['business_id']] = similarity(business_id, df.loc[item]['business_id'], df)
    
    # create list of similarities for top n recommended businesses
    similarity_list = sorted(similarities.items(), key = lambda x: x[1], reverse = True)[:n]
    
    recommendation = []
    required_values = ['business_id', 'stars', 'name', 'city', 'address']
    
    # create a dictionary with usefull data for every recommended business
    for tuple_x, tuple_y in similarity_list:
        
        dictionary = dict()
                
        for item in df.index:
            if df.loc[item]['business_id'] == tuple_x:
                for value in required_values:
                    dictionary[value] = str(df.loc[item][value])        
        
        recommendation.append(dictionary)
        
    return recommendation


# test
recommend(business_id = 'ol2r325YnfuHcq7yeO3vdg')
