# Premier League Winners API

A simple FastAPI application that serves information about Premier League winners from the year 2000 onwards.

## Features

- Get all Premier League winners
- Get winner for a specific season
- Get all wins for a specific team
- Get all wins for a specific manager
- Get general statistics

## Installation

1. Clone or download this project
2. Install the required dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root
- `GET /` - API information and available endpoints

### Winners
- `GET /winners` - Get all Premier League winners
- `GET /winners/{season}` - Get winner for a specific season (e.g., `/winners/2020-2021`)
- `GET /winners/team/{team_name}` - Get all wins for a specific team (e.g., `/winners/team/Manchester City`)
- `GET /winners/manager/{manager_name}` - Get all wins for a specific manager (e.g., `/winners/manager/Pep Guardiola`)

### Statistics
- `GET /stats` - Get general statistics about Premier League winners

## Interactive API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Get all winners
```bash
curl http://localhost:8000/winners
```

### Get winner for 2020-2021 season
```bash
curl http://localhost:8000/winners/2020-2021
```

### Get all Manchester City wins
```bash
curl "http://localhost:8000/winners/team/Manchester City"
```

### Get all Pep Guardiola wins
```bash
curl "http://localhost:8000/winners/manager/Pep Guardiola"
```

### Get statistics
```bash
curl http://localhost:8000/stats
```

## Data Source

The data is stored in `premier_league_winners.json` and includes:
- Season
- Winner team
- Points achieved
- Manager name

Data covers Premier League seasons from 1999-2000 to 2023-2024.
