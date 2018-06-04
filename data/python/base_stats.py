from base_fof import BaseFof
from collections import namedtuple


class BaseStats(BaseFof):
    def get_stage(self, row):
        week = row["Week"]
        stage = namedtuple("stage", ["name", "type"])
        if 1 <= int(week) < 18:
            stage.type = "Regular"
            stage.name = f"Week {week}"
        else:
            stage.type = "Playoffs"
            if int(week) == 18:
                stage.name = "Wildcard"
            elif int(week) == 19:
                stage.name = "Divisional"
            elif int(week) == 20:
                stage.name = "Conference"
            elif int(week) == 21:
                stage.name = "Superbowl"
        return stage