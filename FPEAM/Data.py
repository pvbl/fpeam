import pandas as pd
from .IO import load

from . import utils

LOGGER = utils.logger(name=__name__)


class Data(pd.DataFrame):
    """
    FPEAM data representation.
    """

    COLUMNS = {}
    # @TODO: add method to warn users if column names don't match and what name we choose

    INDEX_COLUMNS = []

    def __init__(self, df=None, fpath=None, columns=COLUMNS):

        _df = pd.DataFrame({}) if df is None and fpath is None else load(fpath=fpath,
                                                                         columns=columns)

        super(Data, self).__init__(data=_df)

        self.source = fpath or 'DataFrame'

        _valid = self.validate()

        try:
            assert _valid is True
        except AssertionError:
            if df is not None or fpath is not None:
                raise RuntimeError('{} failed validation: {}'.format(__name__, _valid))
            else:
                pass
        # else:
        #     if index_columns:
        #         self.set_index(keys=index_columns, inplace=True, drop=True)

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
        _name = type(self).__name__

        _valid = True

        LOGGER.debug('validating %s' % (_name, ))

        if self.empty:
            LOGGER.warning('no data provided for %s' % (_name, ))
            _valid = False

        LOGGER.debug('validated %s' % (_name, ))

        return _valid

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # process exceptions
        if exc_type is not None:
            LOGGER.exception('%s\n%s\n%s' % (exc_type, exc_val, exc_tb))
            return False
        else:
            return self


class Equipment(Data):

    COLUMNS = {'feedstock': str,
               'tillage_type': str,
               'equipment_group': str,
               'rotation_year': int,
               'activity': str,
               'equipment_name': str,
               'equipment_horsepower': float,
               'resource': str,
               'rate': float,
               'unit_numerator': str,
               'unit_denominator': str}

    INDEX_COLUMNS = ('equipment_group', 'feedstock', 'tillage_type', 'equipment_group',
                     'rotation_year', 'activity',
                     'equipment_name', 'equipment_horsepower',
                     'resource', 'unit_numerator', 'unit_denominator')

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(Equipment, self).__init__(df=df, fpath=fpath, columns=columns)


class Production(Data):

    COLUMNS = {'feedstock': str,
               'tillage_type': str,
               'region_production': str,
               'region_destination': str,
               'equipment_group': str,
               'feedstock_measure': str,
               'feedstock_amount': float,
               'unit_numerator': str,
               'unit_denominator': str}

    # @TODO: moves_fips and nonroad_fips columns should be optional and backfilled with NaN if not present

    INDEX_COLUMNS = ('region_production', 'feedstock', 'tillage_type',
                     'equipment_group')

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(Production, self).__init__(df=df, fpath=fpath, columns=columns)


class ResourceDistribution(Data):

    COLUMNS = {'feedstock': str,
               'resource': str,
               'resource_subtype': str,
               'distribution': float}

    INDEX_COLUMNS = ('feedstock', 'resource', 'resource_subtype')

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(ResourceDistribution, self).__init__(df=df, fpath=fpath, columns=columns)


class EmissionFactor(Data):
    COLUMNS = {'resource': str,
               'resource_subtype': str,
               'pollutant': str,
               'rate': float,
               'unit_numerator': str,
               'unit_denominator': str,}

    INDEX_COLUMNS = ('resource', 'resource_subtype', 'pollutant')

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(EmissionFactor, self).__init__(df=df, fpath=fpath, columns=columns)


class FugitiveDust(Data):

    COLUMNS = {'feedstock': str,
               'tillage_type': str,
               'pollutant': str,
               'rate': float,
               'unit_numerator': str,
               'unit_denominator': str}

    INDEX_COLUMNS = ('feedstock', 'tillage_type', 'pollutant',)

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(FugitiveDust, self).__init__(df=df, fpath=fpath, columns=columns)


class SCCCodes(Data):

    COLUMNS = {'name': str,
               'scc': str}

    INDEX_COLUMNS = ('name', )

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(SCCCodes, self).__init__(df=df, fpath=fpath, columns=columns)


class MoistureContent(Data):

    COLUMNS = {'feedstock': str,
               'moisture_content': str}

    INDEX_COLUMNS = ('feedstock', )

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(MoistureContent, self).__init__(df=df, fpath=fpath, columns=columns)


class NONROADEquipment(Data):

    COLUMNS = {'equipment_name': str,
               'equipment_description': str,
               'nonroad_equipment_scc': str}

    INDEX_COLUMNS = ('equipment_name', )

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(NONROADEquipment, self).__init__(df=df, fpath=fpath, columns=columns)


class TransportationGraph(Data):

    COLUMNS = {'edge_id': int,
               'u_of_edge': int,
               'v_of_edge': int,
               'weight': float}

    INDEX_COLUMNS = ('edge_id', )

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(TransportationGraph, self).__init__(df=df, fpath=fpath, columns=columns)


class CountyNode(Data):

    COLUMNS = {'fips': str,
               'node_id': int}

    INDEX_COLUMNS = ('fips', )

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(CountyNode, self).__init__(df=df, fpath=fpath, columns=columns)


class RegionFipsMap(Data):

    COLUMNS = {'region': str,
               'fips': str}

    INDEX_COLUMNS = ('region', )

    def __init__(self, df=None, fpath=None, columns=COLUMNS):
        super(RegionFipsMap, self).__init__(df=df, fpath=fpath, columns=columns)

