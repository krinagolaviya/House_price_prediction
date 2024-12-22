from flask import Flask,request,jsonify
import plotly.graph_objs as go
import util
import pandas as pd

app = Flask(__name__)

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'location' : util.get_location_names()    
    }
    )
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

# @app.route('/get_graph_data', methods=['GET'])
# def get_graph_data():
#     df = util.get_graph_data()
#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=df.iloc[0], y=df.iloc[1], name='Price by Area'))
#     fig.update_layout(title='House Prices by Area', xaxis_title='Area', yaxis_title='Price')

#     graphJSON = fig.to_json()
#     return jsonify(graphJSON).headers.add('Access-Control-Allow-Origin','*')

@app.route('/get_graph_data', methods=['POST'])
def get_graph_data():
    df = util.get_graph_data()
    bhk = int(request.form['bhk'])
    filtered_df = df[df['bhk'] == bhk]
    mean_df = filtered_df.groupby('location')['price'].mean().reset_index()
    sdf = mean_df.sort_values(by="price")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sdf['location'], y=sdf['price'], name='Price by Area'))
    fig.update_layout(title='House Prices by Area', xaxis_title='Area', yaxis_title='Price(lakh)')

    graphJSON = fig.to_json()
    
    # Create response object and add the CORS header
    response = jsonify(graphJSON)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price',methods=['POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bath = int(request.form['bath'])
    bhk = int(request.form['bhk'])
    response = jsonify({
        'estimated_price' : f'{util.get_estimated_price(location,total_sqft,bath,bhk)} Lakh',
        'extra' : ""
    }) if total_sqft>=700 else jsonify({
        'estimated_price' : "Invalid entry",
        'extra' : "Area should be greater than 700 sq feet"
    })
    response.headers.add("Access-Control-Allow-Origin",'*')
    return response

if __name__ == "__main__":
    print("starting python Flask server for home price prediction")
    app.run()