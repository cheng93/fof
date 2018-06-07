from base_fof import BaseFof
from collections import namedtuple
import pandas


class BaseStats(BaseFof):
    def get_stage_name_vectorized(self, series):
        stage_map = pandas.Series(
            data=[self.get_stage(i).name for i in range(1, 22)],
            index=range(1,22))
        return series.map(stage_map)

    def get_stage_type_vectorized(self, series):
        stage_map = pandas.Series(
            data=[self.get_stage(i).type for i in range(1, 22)],
            index=range(1,22))

    def get_stage(self, week):
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