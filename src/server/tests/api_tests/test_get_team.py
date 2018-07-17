import pytest
from api.teams.get_team import GetTeamCommand, seasons_query, team_query

@pytest.fixture
def team_id():
    return 1

@pytest.fixture
def get_team_command(mock_db, team_id):
    team_result = {
        "team_id": team_id,
        "team_name": "Falcons",
        "city": "Atlanta",
        "division": "NFC South",
        "wins": 15,
        "loses": 2,
        "ties": 0,
        "win_lose_percent": 0.67,
        "playoff_appearances": 7,
        "conference_wins": 5,
        "superbowl_wins": 3
    }
    mock_db.register_query(team_query(team_id), team_result)

    seasons_result = [
        {
            "team_id": team_id,
            "year": 2015,
            "wins": 12,
            "loses": 1,
            "ties": 0,
            "win_lose_percent": 0.87,
            "standing_name": "Runner Up"
        },
        {
            "team_id": team_id,
            "year": 2016,
            "wins": 15,
            "loses": 3,
            "ties": 0,
            "win_lose_percent": 0.67,
            "standing_name": "Playoffs"
        }
    ]
    mock_db.register_query(seasons_query(team_id), seasons_result)

    return GetTeamCommand(mock_db, team_id)

@pytest.mark.asyncio
async def test_team(get_team_command,team_id):
    (team_actual, seasons_actual) = await get_team_command.execute()

    team_expected = {
        "team_id": team_id,
        "name": "Atlanta Falcons",
        "division": "NFC South",
        "wins": 15,
        "loses": 2,
        "ties": 0,
        "win_lose_percent": 0.67,
        "playoff_appearances": 7,
        "conference_wins": 5,
        "superbowl_wins": 3
    }

    assert team_expected == team_actual

@pytest.mark.asyncio
async def test_seasons(get_team_command,team_id):
    (team_actual, seasons_actual) = await get_team_command.execute()

    seasons_expected = [
        {
            "team_id": team_id,
            "year": 2015,
            "wins": 12,
            "loses": 1,
            "ties": 0,
            "win_lose_percent": 0.87,
            "standing_name": "Runner Up"
        },
        {
            "team_id": team_id,
            "year": 2016,
            "wins": 15,
            "loses": 3,
            "ties": 0,
            "win_lose_percent": 0.67,
            "standing_name": "Playoffs"
        }
    ]

    assert seasons_expected == seasons_actual
