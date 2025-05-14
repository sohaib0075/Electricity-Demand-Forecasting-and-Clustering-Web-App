# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from model_logic import forecast, cluster, NumpyEncoder
import traceback
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/forecast', methods=['POST'])
def forecast_endpoint():
    try:
        data = request.get_json()
        result = forecast(
            data['city'], data['start_date'], data['end_date'],
            data['model'], data.get('params', {})
        )
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/cluster', methods=['POST'])
def cluster_endpoint():
    try:
        data = request.get_json()
        result = cluster(
            data['city'], data['start_date'], data['end_date'], data['k']
        )
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

#  Use custom JSONProvider for NumPy support
if __name__ == '__main__':
    from flask.json.provider import DefaultJSONProvider

    class CustomJSONProvider(DefaultJSONProvider):
        def dumps(self, obj, **kwargs):
            return json.dumps(obj, cls=NumpyEncoder, **kwargs)
        def loads(self, s, **kwargs):
            return json.loads(s, **kwargs)

    app.json = CustomJSONProvider(app)
    app.run(debug=True, port=5000)
