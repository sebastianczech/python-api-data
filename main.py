from fastapi import FastAPI, HTTPException
from typing import List, Optional
import json
import os
from pathlib import Path

app = FastAPI(
    title="Premier League Winners API",
    description="A simple API to get Premier League winners from 2000 onwards",
    version="1.0.0"
)

# Path to the JSON data file
DATA_FILE = Path(__file__).parent / "premier_league_winners.json"

def load_data():
    """Load Premier League winners data from JSON file"""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON data")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Premier League Winners API",
        "description": "Get information about Premier League winners from 2000 onwards",
        "endpoints": [
            "/winners - Get all Premier League winners",
            "/winners/{season} - Get winner for a specific season",
            "/winners/team/{team_name} - Get all wins for a specific team",
            "/winners/manager/{manager_name} - Get all wins for a specific manager"
        ]
    }

@app.get("/winners")
async def get_all_winners():
    """Get all Premier League winners from 2000 onwards"""
    data = load_data()
    return {
        "total_seasons": len(data),
        "winners": data
    }

@app.get("/winners/{season}")
async def get_winner_by_season(season: str):
    """Get Premier League winner for a specific season (e.g., '2020-2021')"""
    data = load_data()
    
    for winner in data:
        if winner["season"] == season:
            return winner
    
    raise HTTPException(status_code=404, detail=f"No data found for season {season}")

@app.get("/winners/team/{team_name}")
async def get_wins_by_team(team_name: str):
    """Get all Premier League wins for a specific team"""
    data = load_data()
    
    team_wins = [winner for winner in data if winner["winner"].lower() == team_name.lower()]
    
    if not team_wins:
        raise HTTPException(status_code=404, detail=f"No wins found for team {team_name}")
    
    return {
        "team": team_name,
        "total_wins": len(team_wins),
        "seasons": team_wins
    }

@app.get("/winners/manager/{manager_name}")
async def get_wins_by_manager(manager_name: str):
    """Get all Premier League wins for a specific manager"""
    data = load_data()
    
    manager_wins = [winner for winner in data if manager_name.lower() in winner["manager"].lower()]
    
    if not manager_wins:
        raise HTTPException(status_code=404, detail=f"No wins found for manager {manager_name}")
    
    return {
        "manager": manager_name,
        "total_wins": len(manager_wins),
        "seasons": manager_wins
    }

@app.get("/stats")
async def get_statistics():
    """Get general statistics about Premier League winners"""
    data = load_data()
    
    # Count wins by team
    team_wins = {}
    manager_wins = {}
    highest_points = 0
    lowest_points = float('inf')
    highest_points_season = ""
    lowest_points_season = ""
    
    for winner in data:
        team = winner["winner"]
        manager = winner["manager"]
        points = winner["points"]
        
        # Team statistics
        team_wins[team] = team_wins.get(team, 0) + 1
        
        # Manager statistics
        manager_wins[manager] = manager_wins.get(manager, 0) + 1
        
        # Points statistics
        if points > highest_points:
            highest_points = points
            highest_points_season = winner["season"]
        
        if points < lowest_points:
            lowest_points = points
            lowest_points_season = winner["season"]
    
    # Sort teams and managers by wins
    sorted_teams = sorted(team_wins.items(), key=lambda x: x[1], reverse=True)
    sorted_managers = sorted(manager_wins.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "total_seasons": len(data),
        "teams_by_wins": sorted_teams,
        "managers_by_wins": sorted_managers,
        "highest_points": {
            "points": highest_points,
            "season": highest_points_season
        },
        "lowest_points": {
            "points": lowest_points,
            "season": lowest_points_season
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
