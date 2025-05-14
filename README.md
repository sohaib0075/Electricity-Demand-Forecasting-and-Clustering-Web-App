# Electricity-Demand-Forecasting-and-Clustering-Web-App
A full-stack web application for forecasting electricity demand using machine learning models and analyzing demand patterns via clustering. Supports Random Forest, XGBoost, and LSTM models with interactive Plotly visualizations.
---

## 🌐 Live Features

- 📈 **Demand Forecasting** (Hourly):  
  Predict demand using RF, XGB, or LSTM for any date range and city.

- 🔍 **Clustering Analysis**:  
  Use K-Means to group similar demand patterns for a city and period.

- 🧠 **Synthetic Data Simulation**:  
  Demand data is generated for demonstration (real data integration-ready).

- 🖼️ **Plotly Visualizations**:  
  Interactive, browser-based charts for demand vs prediction and clusters.

---

## 🛠️ Tech Stack

| Layer      | Technology                     |
|------------|--------------------------------|
| Frontend   | HTML, CSS (Bootstrap), JS      |
| Backend    | Flask (Python) + Flask-CORS    |
| Models     | RandomForest, XGBoost, LSTM    |
| Visuals    | Plotly                          |
| Clustering | K-Means (Scikit-learn)         |

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/powerscope.git
cd powerscope
