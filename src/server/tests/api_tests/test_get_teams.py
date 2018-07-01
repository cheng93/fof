import pytest
from api.teams.get_teams import GetTeamsCommand, teams_query

@pytest.fixture
def get_teams_command(mock_db):
    teams_result = [
        {
            "team_id": 1,
            "city": "Atlanta",
            "team_name": "Falcons",
            "wins": 12,
            "loses": 1,
            "ties": 0,
            "win_lose_percent": 0.87,
            "playoff_appearances": 9,
            "conference_wins": 5,
            "superbowl_wins": 3
        },
        {
            "team_id": 2,
            "city": "New Orleans",
            "team_name": "Saints",
            "wins": 2,
            "loses": 11,
            "ties": 2,
            "win_lose_percent": 0.04,
            "playoff_appearances": 1,
            "conference_wins": 0,
            "superbowl_wins": 0
        }
    ]
    mock_db.register_query(teams_query(), teams_result)

    return GetTeamsCommand(mock_db)

@pytest.mark.asyncio
async def test_command(get_teams_command):
    actual = await get_teams_command.execute()

    expected = [
        {
            "team_id": 1,
            "name": "Atlanta Falcons",
            "wins": 12,
            "loses": 1,
            "ties": 0,
            "win_lose_percent": 0.87,
            "playoff_appearances": 9,
            "conference_wins": 5,
            "superbowl_wins": 3
        },
        {
            "team_id": 2,
            "name": "New Orleans Saints",
            "wins": 2,
            "loses": 11,
            "ties": 2,
            "win_lose_percent": 0.04,
            "playoff_appearances": 1,
            "conference_wins": 0,
            "superbowl_wins": 0
        }
    ]

    assert expected == actual
