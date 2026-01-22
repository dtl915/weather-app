# Weather App

A Flask-based web application for querying historical weather data for Chinese cities. The app scrapes weather data from tianqihoubao.com and caches it in a MySQL database.

## Features

- Query historical weather data by city and date
- Automatic data caching in MySQL database
- Morning and night weather information (temperature, weather conditions, wind)
- Input validation (prevents future date queries)
- JSON API responses

## Requirements

- Python 3.x
- MySQL Server

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd weather-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
```sql
CREATE DATABASE weather_db;
```

4. Update the database connection in `app.py` if needed:
```python
DATABASE_URL = "mysql+pymysql://root:your_password@localhost:3306/weather_db?charset=utf8mb4"
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with weather query form |
| POST | `/weather` | Query weather data (params: `city`, `date`) |

## Database Schema

**Table: `weather_data`**

| Column | Type | Description |
|--------|------|-------------|
| city | VARCHAR(45) | City name (Primary Key) |
| date | DATE | Weather date (Primary Key) |
| morning_temp | VARCHAR(45) | Morning temperature |
| night_temp | VARCHAR(45) | Night temperature |
| morning_weather | VARCHAR(45) | Morning weather condition |
| night_weather | VARCHAR(45) | Night weather condition |
| morning_wind | VARCHAR(45) | Morning wind info |
| night_wind | VARCHAR(45) | Night wind info |

## Dependencies

- Flask
- requests
- beautifulsoup4
- lxml
- SQLAlchemy
- PyMySQL
