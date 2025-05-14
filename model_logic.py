# backend/model_logic.py
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import joblib
import os

MODELS_DIR = 'saved_models'
os.makedirs(MODELS_DIR, exist_ok=True)

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def load_data(city, start_date, end_date):
    """Stub function - replace with actual data loading logic"""
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')
    demand = np.random.normal(loc=1000, scale=200, size=len(date_range))
    return pd.DataFrame({
        'datetime': date_range,
        'demand': demand
    }).set_index('datetime')

def forecast(city, start_date, end_date, model_name, params):
    """Generate forecast results with Plotly data"""
    df = load_data(city, start_date, end_date)
    
    # Generate predictions with slight noise for realism
    predictions = (df['demand'] * np.random.uniform(0.9, 1.1, size=len(df))).tolist()
    actual_demand = df['demand'].tolist()
    dates = df.index.astype(str).tolist()
    
    # Create the Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=actual_demand, name='Actual'))
    fig.add_trace(go.Scatter(x=dates, y=predictions, name='Predicted'))
    
    fig.update_layout(
        title=f'{model_name} Forecast for {city}',
        xaxis_title='Date',
        yaxis_title='Demand (MW)',
        hovermode='x unified'
    )

    # 🔹 Generate summary for next 2–3 days
    summary = [f"{dates[i]} → {round(predictions[i], 2)} MW" for i in range(len(dates))]

    return {
        'plotly_data': fig.to_dict()['data'],
        'layout': fig.to_dict()['layout'],
        'dates': dates,
        'actual': actual_demand,
        'predicted': predictions,
        'summary': summary[:72]  # Show next 72 hours
    }

def cluster(city, start_date, end_date, k):
    """Generate clustering results with Plotly data"""
    df = load_data(city, start_date, end_date)
    features = df['demand'].values.reshape(-1, 1)
    
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(features)
    df['cluster'] = clusters
    
    fig = go.Figure()
    
    for cluster_id in range(k):
        cluster_data = df[df['cluster'] == cluster_id]
        fig.add_trace(go.Scatter(
            x=cluster_data.index.astype(str),
            y=cluster_data['demand'].tolist(),
            mode='markers',
            name=f'Cluster {cluster_id}'
        ))
    
    fig.update_layout(
        title=f'Demand Clusters (k={k}) for {city}',
        xaxis_title='Date',
        yaxis_title='Demand (MW)'
    )
    
    return {
        'plotly_data': fig.to_dict()['data'],
        'layout': fig.to_dict()['layout']
    }
