import pandas as pd
import numpy as np
import joblib
from joblib import load  
from flask import Flask, jsonify, request
import yfinance as yf


app = Flask(__name__)


@app.route("/", methods=["GET"])
def make_prediction():
    cols_bin = []
    vols_bin = []

    try:
        loaded_model = joblib.load("RF_BTC_1D.joblib")

        
        data = yf.download("BTC-USD", period="19d")

        
        data['Date'] = data.index
        data = data.reset_index(drop=True)
        data = data[["Date", "Adj Close", "Volume"]].rename(columns={"Adj Close": "Close"})
        data['returns'] = np.log(data['Close'] / data['Close'].shift(1)) 
        data.dropna(inplace=True) 
        data['direction'] = np.sign(data['returns']).astype(int)
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

        def create_bins(data, bins=[0]):
            nonlocal cols_bin
            nonlocal cols
            for col in cols:
                col_bin = col + '_bin'
                data[col_bin] = np.digitize(data[col], bins=bins)
                cols_bin.append(col_bin)

        create_bins(data)
        data[cols+cols_bin].head(2)

        def create_bins_v(data, bins=[0]):
            nonlocal vols_bin
            nonlocal vols
            for vol in vols:
                vol_bin = vol + '_bin'
                data[vol_bin] = np.digitize(data[vol], bins=bins)
                vols_bin.append(vol_bin)
        
        create_bins_v(data)
        data[vols+vols_bin].head(2)

        cols_bin = cols_bin+vols_bin
        if len(data) > 0: 
            predictions = loaded_model.predict(data[cols_bin])
            predictions_int = predictions.astype(int)
            return jsonify({"predictions": predictions_int.tolist()})
        else:
            return jsonify({"error": "No data for prediction"}), 400  

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int("5000"))