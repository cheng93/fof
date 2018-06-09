from sqlalchemy import Column, ForeignKey, Integer, MetaData, Table, text

metadata = MetaData()


player_history = Table(
    'player_history', metadata,
    Column('player_history_id', Integer, primary_key=True, server_default=text(
        "nextval('player_history_player_history_id_seq'::regclass)")),
    Column('player_id', ForeignKey('player.player_id'), nullable=False),
    Column('year', ForeignKey('year.year'), nullable=False),
    Column('stage_id', ForeignKey('stage.stage_id'), nullable=False),
    Column('old_team_id', ForeignKey('team.team_id')),
    Column('new_team_id', ForeignKey('team.team_id'))
)
