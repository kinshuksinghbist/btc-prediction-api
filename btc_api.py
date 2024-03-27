import pandas as pd
import numpy as np
import joblib
from joblib import load  # Import joblib for loading
from flask import Flask, jsonify, request
import yfinance as yf


app = Flask(__name__)


@app.route("/predict", methods=["GET"])
def make_prediction():
    cols_bin = []
    vols_bin = []

    try:
        loaded_model = joblib.load("RF_BTC_1D.joblib")

        # Download data
        data = yf.download("BTC-USD", period="19d")

        # Preprocess data
        data['Date'] = data.index
        data = data.reset_index(drop=True)
        data = data[["Date", "Adj Close", "Volume"]].rename(columns={"Adj Close": "Close"})
        data['returns'] = np.log(data['Close'] / data['Close'].shift(1))  # Calculate pct returns
        data.dropna(inplace=True)  # Drop rows with missing values
        data['direction'] = np.sign(data['returns']).astype(int)  # Assign direction to changes
        data['pct_change_v'] = np.log(data['Volume'] / data['Volume'].shift(1))
        data.dropna(inplace=True)
        lags = [1, 2, 3, 4, 5, 6, 7, 8]
        cols = []
        for lag in lags:
            col = f'rtn_lag{lag}'
            data[col] = data['returns'].shift(lag)
            cols.append(col)
        data.dropna(inplace=True)
        vols = []
        for lag in lags:
            vol = f'v_lag{lag}'
            data[vol] = data['pct_change_v'].shift(lag)
            vols.append(vol)
        data.dropna(inplace=True)

        # Feature Engineering (potential fix)
        def create_bins(data, bins=[0]):
            nonlocal cols_bin
            nonlocal cols
            for col in cols:
                col_bin = col + '_bin'
                data[col_bin] = np.digitize(data[col], bins=bins)
                cols_bin.append(col_bin)  # Return the created bins

        create_bins(data)
        data[cols+cols_bin].head(2)

        def create_bins_v(data, bins=[0]):
            nonlocal vols_bin
            nonlocal vols
            for vol in vols:
                vol_bin = vol + '_bin'
                data[vol_bin] = np.digitize(data[vol], bins=bins)
                vols_bin.append(vol_bin)# Pass a copy of data to avoid modifying original
        # Prediction
        create_bins_v(data)
        data[vols+vols_bin].head(2)

        cols_bin = cols_bin+vols_bin
        if len(data) > 0:  # Check if there's any data for prediction
            predictions = loaded_model.predict(data[cols_bin])
            predictions_int = predictions.astype(int)
            return jsonify({"predictions": predictions_int.tolist()})
        else:
            return jsonify({"error": "No data for prediction"}), 400  # Return specific error

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)