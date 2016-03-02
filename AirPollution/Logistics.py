# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 1:02:31 2016

Populates tables for logistics emissions and electricity consumption associated with feedstock processing

Inputs include:
    list of feedstock types (feedstock_list)
    container (cont)

@author: aeberle
"""

import SaveDataHelper
from src.AirPollution.utils import config, logger


class Logistics(SaveDataHelper.SaveDataHelper):
    """
    Computes the emissions and electricity use associated with feedstock processing
    Only emissions are VOC from wood drying (forestry only)
    Electricity is tabulated to compute total kWh by feedstock type
    """

    def __init__(self, feedstock_list, cont):
        """

        :param feedstock_list: list of feedstocks to process
        :param cont: Container object
        :return:
        """
        SaveDataHelper.SaveDataHelper.__init__(self, cont)
        self.feedstock_list = feedstock_list
        self.document_file = "Logistics"  # gets used to save query to a text file for debugging purposes
        self.electricity_per_dt = config.get('electricity_per_dt')  # electricity dictionary
        self.logistics_type = config.get('logistics_type')  # logistics method (A = advanced, C = conventional)

        self.kvals = dict()
        # set production schema and scenario name
        self.kvals['production_schema'] = config.get('production_schema')
        self.kvals['scenario_name'] = config.get('title')

        self.column_dict = dict()
        # create dictionary for column names for production data
        self.column_dict['CG'] = 'total_prod'
        self.column_dict['CS'] = 'prod'
        self.column_dict['WS'] = 'prod'
        self.column_dict['SG'] = 'prod'
        self.column_dict['FR'] = 'fed_minus_55'

        # dictionary for VOC emission factor from wood drying
        self.voc_wood_ef = config.get('voc_wood_ef')

    def electricity(self, feed):
        """
        Tally electricity consumption from feedstock processing
        Update logistics table with these values

        Equation for computing electricity consumption (generated by Ethan Warner):

        E = B * electricity_per_dt

        E = electricity (kWh per year per county)
        B = biomass production (dry short ton per yr per county)
        electricity_per_dt = electricity consumed (kWh per dry short ton?

        :param feed: feedstock
        :return: True if update query is successful, False if not
        """

        logger.debug('Calculating electricity consumption for {feed}'.format(feed=feed))
        # set electricity consumption factor using feedstock type
        self.kvals['electricity_per_dt'] = self.electricity_per_dt[feed][self.logistics_type]
        # set feedstock name
        self.kvals['feed'] = feed
        # set column for production name
        self.kvals['column'] = self.column_dict[feed]

        # generate string for query
        # @TODO: change query to use new table for FIPS code associated with processing rather than production (these data need to be imported into the database first)
        query = """INSERT INTO {scenario_name}.{feed}_logistics (fips, electricity)
                SELECT feed.fips,
                feed.{column} * {electricity_per_dt} AS "electricity"
                FROM {production_schema}.{feed}_data feed
                GROUP BY feed.fips;""".format(**self.kvals)

        # execute query
        return self._execute_query(query)

    def voc_wood_drying(self, feed):
        """
        Compute VOC emissions from wood drying
        Only applies to forestry

        Equation for computing VOC emissions from wood drying (generated by Ethan Warner):

        VOC = (B * a) * (VOC_ef) / b

        VOC = VOC emissions (metric tons per year per county)
        B = biomass production (dry short ton per yr per county)
        a = constant (0.9071847 metric tons per short ton)
        VOC_ef = emission factor for VOC (kg per dry metric ton of feedstock)
        b = constant (1000 kg per metric ton)

        :param feed: feedstock
        :return: True if update query is successful, False if not
        """

        logger.info('Computing VOC emissions from wood drying')

        # set constants a and b (see equation above for more details)
        self.kvals['a'] = 0.9071847  # metric ton per short ton
        self.kvals['b'] = 1000.0  # kg per metric ton

        # set VOC emission factor
        self.kvals['VOC_ef'] = self.voc_wood_ef[self.logistics_type]
        # set feedstock name
        self.kvals['feed'] = feed
        # set column for production name
        self.kvals['column'] = self.column_dict[feed]

        # generate string for query and append to queries
        # @TODO: change query to use new table for FIPS code associated with processing rather than production (these data need to be imported into the database first)
        query = """UPDATE {scenario_name}.{feed}_logistics
                SET VOC = prod_data.{column} * {a} * {VOC_ef} / {b}
                FROM {production_schema}.{feed}_data prod_data
                WHERE {scenario_name}.{feed}_logistics.fips = prod_data.fips;""".format(**self.kvals)

        return self._execute_query(query)

    def loading_equip(self, feed):
        """

        :param feed: feedstock
        :return:
        """
        # @TODO: insert functionality for processing output from NONROAD for logistics equipment (tractors for loading agricultural crops; chipper/loader for forestry)
        logger.warning('Loading equipment processing functionality has not been implemented')
        pass

    def calc_logistics(self):
        # Execute wood drying and electricity functions for all feedstocks in feedstock list
        logger.info('Evaluating logistics')
        for feed in self.feedstock_list:
            logger.debug('Calculating electricity for %s' % (feed, ))
            self.electricity(feed)
            logger.debug('Processing loading equipment for %s' % (feed, ))
            self.loading_equip(feed)
            if feed == 'FR':
                logger.debug("Calculating wood drying VOC")
                self.voc_wood_drying(feed)
