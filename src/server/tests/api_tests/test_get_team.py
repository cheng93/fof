import pytest
from api.teams.get_team import GetTeamCommand, team_query

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

    return GetTeamCommand(mock_db, team_id)

@pytest.mark.asyncio
async def test_team(get_team_command,team_id):
    team_actual = await get_team_command.execute()

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