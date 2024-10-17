---

# 🚀 Cryptocurrency Prediction API with Docker and Flask

![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Joblib](https://img.shields.io/badge/Joblib-lightgrey?logo=joblib)
![yFinance](https://img.shields.io/badge/yFinance-brightgreen)

This project contains a machine learning-based cryptocurrency prediction API using Flask, Docker, and a pre-trained `joblib` model. The API retrieves recent Bitcoin data using the `yfinance` library, performs preprocessing, and serves predictions through a simple REST interface.

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Docker](#-docker-setup)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)

## ✨ Features
- 📊 **Bitcoin price prediction** using a pre-trained machine learning model.
- 🔧 **Preprocessing pipeline** including log returns, lags, and binning of features.
- 🛠️ **Dockerized application** for easy deployment and scalability.
- ⚡ **Flask API** to serve predictions via HTTP.
- 🧠 **Model storage** using `joblib` for fast and efficient prediction serving.

## 🛠️ Tech Stack
- **Flask** - Python micro-framework to serve the API.
- **Joblib** - Efficient serialization of the trained machine learning model.
- **yFinance** - Data retrieval for cryptocurrency (Bitcoin) prices.
- **Docker** - Containerization for portability and easy deployment.

## 📂 Project Structure

```bash
.
├── Dockerfile                # Dockerfile to build the API container
├── app.py                    # Flask API implementation
├── RF_BTC_1D.joblib          # Pre-trained machine learning model
├── requirements.txt          # Dependencies for the project
└── README.md                 # Project documentation
```

## 🐳 Docker Setup

1. **Install Docker**: Make sure you have Docker installed on your system. You can download it [here](https://www.docker.com/products/docker-desktop).
   
2. **Build the Docker Image**:
    ```bash
    docker build -t crypto-prediction-api .
    ```

3. **Run the Docker Container**:
    ```bash
    docker run -d -p 5000:5000 crypto-prediction-api
    ```

4. The API will now be available at `http://localhost:5000`.

## ⚙️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/crypto-prediction-api.git
    ```

2. Navigate to the project directory:
    ```bash
    cd crypto-prediction-api
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask app locally:
    ```bash
    python app.py
    ```

The API will now be running locally at `http://localhost:5000`.

## 🚀 Usage

Once the API is up and running, you can use the following endpoint:

### GET `/`
Fetches the latest Bitcoin data and returns a prediction based on the pre-trained model.

#### Example Request:
```bash
curl http://localhost:5000/
```

#### Example Response:
```json
{
    "predictions": [1, -1, 1, 1, -1, 1]
}
```

## 📈 API Endpoints

| HTTP Method | Endpoint | Description                           |
|-------------|----------|---------------------------------------|
| `GET`       | `/`      | Returns predicted Bitcoin price moves |

## 🏗️ Model & Preprocessing

- **Data Retrieval**: We use the `yfinance` library to retrieve Bitcoin data for the past 19 days.
- **Preprocessing**: The model applies several transformations to the data:
  - **Log Returns**: Calculates the log of the price changes.
  - **Lags**: Adds lag features to capture temporal dependencies.
  - **Binning**: Converts continuous features into bins to make predictions easier.
  
The model is pre-trained and saved in the `RF_BTC_1D.joblib` file. It's a Random Forest classifier that predicts the future direction of Bitcoin price changes.

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Push to your branch and submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
