import argparse
import psycopg2


parser = argparse.ArgumentParser(description="Convert fof csvs to sql.")
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

cur.execute("""
    TRUNCATE stats.punting CASCADE
    ;

    TRUNCATE stats.kicking CASCADE
    ;

    TRUNCATE stats.defending CASCADE
    ;

    TRUNCATE stats.blocking CASCADE
    ;

    TRUNCATE stats.fumbles CASCADE
    ;

    TRUNCATE stats.returning CASCADE
    ;

    TRUNCATE stats.receiving CASCADE
    ;

    TRUNCATE stats.rushing CASCADE
    ;

    TRUNCATE stats.passing CASCADE
    ;

    TRUNCATE player_history CASCADE
    ;

    TRUNCATE staff_history CASCADE
    ;

    TRUNCATE staff CASCADE
    ;

    TRUNCATE draft CASCADE
    ;

    TRUNCATE player CASCADE
    ;

    TRUNCATE game CASCADE
    ;

    TRUNCATE year CASCADE
    ;
""")

conn.commit()
cur.close()
conn.close()