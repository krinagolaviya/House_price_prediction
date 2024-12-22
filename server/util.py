import pickle
import json
import numpy as np
import pandas as pd
__locations = None
__data_columns = None
__model = None
__df = pd.DataFrame()
__rawdf = None
__similarity = None

def get_estimated_price(location,sqft,bhk,bath):
    load_saved_artifacts()

    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __df
    global __rawdf
    global __similarity

    with open("./artifacts/bangaluru_price_predict_model_columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./artifacts/bangaluru_price_predict_model.pickle', 'rb') as f:
            __model = pickle.load(f)

    # with open('./artifacts/graph_data.pickle', 'rb') as f:
    #     __df = pickle.load(f)
    with open('./artifacts/raw_data.pickle', 'rb') as f:
        __rawdf = pickle.load(f)
    
    with open('./artifacts/similarity.pickle', 'rb') as f:
        __similarity = pickle.load(f)
    

    with open('./artifacts/df.pkl', 'rb') as f:
        __df = pickle.load(f)
    print("loading saved artifacts...done")
    
    

def get_recommanded_data(location):
    global __df
    load_saved_artifacts()
    location = location.strip().lower()
    __df['location'] = __df['location'].str.strip().str.lower()

    filtered_df = __df[__df['location'] == location]
    if filtered_df.empty:
        return f"Location '{location}' not found in the dataset."
    # print(__df[__df['location'] == location])
    # index = __df[__df['location'] == location].index[0]
    index = filtered_df.index[0]
    location_list = sorted(list(enumerate(__similarity[index])),reverse=True,key = lambda x : x[1])[1:6]
    recommanded_location = []
    for i in location_list:
        recommanded_location.append(__df.iloc[i[0]].location)

    return recommanded_location

def get_graph_data():
    load_saved_artifacts()
    return __rawdf

def get_location_names():
    load_saved_artifacts()

    return __locations

def get_data_columns():
    load_saved_artifacts()

    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location
    print(__df)