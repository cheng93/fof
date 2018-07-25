import pytest
from api.teams.get_seasons import GetSeasonsCommand, seasons_query

@pytest.fixture
def team_id():
    return 1

@pytest.fixture
def get_seasons_command(mock_db, team_id):
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

    return GetSeasonsCommand(mock_db, team_id)

@pytest.mark.asyncio
async def test_seasons(get_seasons_command,team_id):
    seasons_actual = await get_seasons_command.execute()

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