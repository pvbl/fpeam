import pandas as pd
from IO import load
from collections import OrderedDict


class Data(pd.DataFrame):
    """
    Equipment budget representation.
    """

    COLUMNS = {}

    def __init__(self, df=None, fpath=None, columns=COLUMNS):

        _df = df or load(fpath=fpath, columns=columns)

        super(Data, self).__init__(data=_df, index=None)

        # error if mandatory missing
        # coerce types
        # error if not able to coerce
        # backfill non-mandatory missing

    def backfill(self):
        # @TODO: add backfill methods
        raise NotImplementedError

    def summarize(self):
        # @TODO: add summarization methods
        raise NotImplementedError

    def validate(self):

        # @TODO: add validation methods
        raise NotImplementedError


class Budget(Data):

    COLUMNS = OrderedDict((('id', str),
                           ('feedstock', str),
                           ('tillage', str),
                           ('region_id', str),
                           ('rotation_year', str),
                           ('operation_unit', str),
                           ('activity', str),
                           ('equipment_name', str),
                           ('equipment_hp', float),
                           ('capacity', float),
                           ('resource', str),
                           ('rate', float),
                           ('unit', str)))

# id, feedstock, tillage, region_id, rotation_year, operation_unit, activity, equipment_name, equipment_hp, capacity, resource, rate, unit

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(Budget, self).__init__(df=df, fpath=fpath, columns=columns)


class Production(Data):

    COLUMNS = OrderedDict((('region_id', str),
                           ('feedstock', str),
                           ('tillage', str),
                           ('yield', float)))

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(Production, self).__init__(df=df, fpath=fpath, columns=columns)
