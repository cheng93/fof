import argparse
import psycopg2

from draft import Draft
from game import Game
from player import Player
from player_history import PlayerHistory
from staff import Staff
from staff_history import StaffHistory
from stats_blocking import StatsBlocking
from stats_defending import StatsDefending
from stats_fumbles import StatsFumbles
from stats_kicking import StatsKicking
from stats_passing import StatsPassing
from stats_punting import StatsPunting
from stats_receiving import StatsReceiving
from stats_returning import StatsReturning
from stats_rushing import StatsRushing
import year

parser = argparse.ArgumentParser(description="Convert fof csvs to sql.")
parser.add_argument("-y", dest="year", required=True)
parser.add_argument("-s",dest="staff_id", required=True)
parser.add_argument("-d",dest="db", required=True)
parser.add_argument("-ho",dest="host", required=True)
parser.add_argument("-p",dest="port", required=True)
parser.add_argument("-u",dest="user", required=True)
parser.add_argument("-pa",dest="password")
args = parser.parse_args()

try:
    conn = psycopg2.connect(
            dbname=args.db,
            user=args.user,
            host=args.host,
            port=args.port,
            password=args.password)
except:
    print("Couldn't connect")
cur = conn.cursor()

print(args.year)

cur.execute(year.execute(args.year))

game_import = Game()
game_import.execute(cur, args.year)

player_import = Player()
player_import.execute(cur, args.year)

draft_import = Draft()
draft_import.execute(cur, args.year)

staff_import = Staff()
staff_import.execute(cur, args.year, args.staff_id)

staff_history_import = StaffHistory()
staff_history_import.execute(cur, args.year)

player_history_import = PlayerHistory()
player_history_import.execute(cur, args.year)

stats_passing_import = StatsPassing()
stats_passing_import.execute(cur, args.year)

stats_rushing_import = StatsRushing()
stats_rushing_import.execute(cur, args.year)

stats_receiving_import = StatsReceiving()
stats_receiving_import.execute(cur, args.year)

stats_returning_import = StatsReturning()
stats_returning_import.execute(cur, args.year)

stats_fumbles_import = StatsFumbles()
stats_fumbles_import.execute(cur, args.year)

stats_blocking_import = StatsBlocking()
stats_blocking_import.execute(cur, args.year)

stats_defending_import = StatsDefending()
stats_defending_import.execute(cur, args.year)

stats_kicking_import = StatsKicking()
stats_kicking_import.execute(cur, args.year)

stats_punting_import = StatsPunting()
stats_punting_import.execute(cur, args.year)

conn.commit()
cur.close()
conn.close()