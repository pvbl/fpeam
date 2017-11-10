# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 1:02:31 2016
Prototyped on Wednesday November 8 2017

- Computes the emissions and electricity use associated with feedstock
processing
- Only emissions are VOC from wood drying (forestry only)
- Electricity is tabulated to compute total kWh by feedstock type and fips

@author: aeberle, rhanes
"""

import pandas as pd

# @TODO remove when finalizing
import os

class Logistics:

    def __init__(self):
        """
        Prototype edition:
        Defines electricity usage (kWh) per dry ton
        Defines VOC emission factors for wood drying
        Reads in relevant columns from all transport data tables,
        adds identification columns and binds together into one transport table

        Final edition:
        Pulls in electricity usage (kWh) per dry ton from default or
        user-defined data set
        Pulls in VOC emission factors for wood drying from default or
        user-defined data set
        Pulls in relevant columns from default or user-defined transport
        data tables, adds ID columns and binds together

        :return:
        """

        # hard-coded electricity usage (kWh) per dry ton biomass under
        # conventional and advanced logistics
        self.electricity_per_dt = pd.DataFrame({'feed_id': ['Corn stover',
                                                             'Corn stover',
                                                             'Wheat straw',
                                                             'Wheat straw',
                                                             'Switchgrass',
                                                             'Switchgrass',
                                                             'Miscanthus',
                                                             'Miscanthus',
                                                             'Corn grain',
                                                             'Corn grain',
                                                             'Sorghum stubble',
                                                             'Sorghum stubble',
                                                             'Residues',
                                                             'Residues',
                                                             'Whole tree',
                                                             'Whole tree'],
                                                'logistics_type': ['conv',
                                                                   'adv',
                                                                   'conv',
                                                                   'adv',
                                                                   'conv',
                                                                   'adv',
                                                                   'conv',
                                                                   'adv',
                                                                   'conv',
                                                                   'adv',
                                                                   'conv',
                                                                   'adv',
                                                                   'conv',
                                                                   'adv',
                                                                   'conv',
                                                                   'adv',],
                                                 'kWh_per_dt': [36.0, 188.5,
                                                                36.0, 188.5,
                                                                36.0, 188.5,
                                                                36.0, 188.5,
                                                                36.0, 188.5,
                                                                21.0, 173.5,
                                                                40.0, 191.5,
                                                                40.0, 191.5]})

        # hard-coded VOC emission factors for wood drying
        # @todo what are these units, kg/metric ton?
        self.voc_wood_ef = pd.DataFrame({'feed_id': ['Residues', 'Residues',
                                                     'Whole tree',
                                                     'Whole tree'],
                                         'logistics_type': ['conv', 'adv',
                                                            'conv', 'adv'],
                                         'hammer_mill_ef': [0.52, 0.52,
                                                            0.52, 0.52],
                                         'grain_dryer_ef': [0.0, 0.23,
                                                            0.0, 0.23]})

        ## read in the four relevant transport tables for 2040,
        # add three extra ID columns for year, logistics type and yield
        # type, then bind together into one comprehensive transport
        # table for use elsewhere
        transport_herb_bc_adv = pd.read_csv(os.getcwd()\
                                            + '\\input_data\\' \
                                            + 'logistics_transport_data' \
                                            + '\\transport_herb_bc_adv_' \
                                            + '2040.csv',
                                            usecols = ['feed_id',
                                                       'sply_fips',
                                                       'used_qnty'])
        transport_herb_bc_adv['year'] = 2040
        transport_herb_bc_adv['logistics_type'] = 'adv'
        transport_herb_bc_adv['yield_type'] = 'bc'

        transport_herb_hh_adv = pd.read_csv(os.getcwd() \
                                              + '\\input_data\\' \
                                              + 'logistics_transport_data' \
                                              + '\\transport_herb_hh_adv_' \
                                              + '2040.csv',
                                             usecols = ['feed_id',
                                                        'sply_fips',
                                                        'used_qnty'])
        transport_herb_hh_adv['year'] = 2040
        transport_herb_hh_adv['logistics_type'] = 'adv'
        transport_herb_hh_adv['yield_type'] = 'hh'

        transport_woody_bc_adv = pd.read_csv(os.getcwd() \
                                             + '\\input_data\\' \
                                             + 'logistics_transport_data' \
                                             +
                                              '\\transport_woody_bc_adv_' \
                                             + '2040.csv',
                                              usecols = ['feed_id',
                                                         'sply_fips',
                                                         'used_qnty'])
        transport_woody_bc_adv['year'] = 2040
        transport_woody_bc_adv['logistics_type'] = 'adv'
        transport_woody_bc_adv['yield_type'] = 'bc'

        transport_woody_hh_adv = pd.read_csv(os.getcwd() \
                                             + '\\input_data\\' \
                                             + 'logistics_transport_data' \
                                             +
                                              '\\transport_woody_hh_adv_' \
                                             + '2040.csv',
                                              usecols = ['feed_id',
                                                         'sply_fips',
                                                         'used_qnty'])
        transport_woody_hh_adv['year'] = 2040
        transport_woody_hh_adv['logistics_type'] = 'adv'
        transport_woody_hh_adv['yield_type'] = 'hh'

        ## Read in the two relevant transport tables for 2017 (only two
        # 2017 tables are in the input data folers), add three id
        # columns for year, logistics type and yield type, then bind
        # together into a comprehensive transport table for use elsewhere
        transport_herb_bc_conv = pd.read_csv(os.getcwd()\
                                              + '\\input_data\\' \
                                              + 'logistics_transport_data' \
                                              + '\\transport_herb_bc_conv_' \
                                              + '2017.csv',
                                              usecols = ['feed_id',
                                                         'sply_fips',
                                                         'used_qnty'])
        transport_herb_bc_conv['year'] = 2017
        transport_herb_bc_conv['logistics_type'] = 'conv'
        transport_herb_bc_conv['yield_type'] = 'bc'

        transport_woody_bc_conv = pd.read_csv(os.getcwd() \
                                             + '\\input_data\\' \
                                             + 'logistics_transport_data' \
                                             + '\\transport_woody_bc_conv_' \
                                             + '2017.csv',
                                              usecols = ['feed_id',
                                                         'sply_fips',
                                                         'used_qnty'])
        transport_woody_bc_conv['year'] = 2017
        transport_woody_bc_conv['logistics_type'] = 'conv'
        transport_woody_bc_conv['yield_type'] = 'bc'

        # bind together all the transport tables
        # this comprehensive table is the only one to get passed around via
        # self
        self.transport = transport_herb_bc_adv.append(
            transport_herb_hh_adv).append(
            transport_woody_bc_adv).append(
            transport_woody_hh_adv).append(
            transport_herb_bc_conv).append(transport_woody_bc_conv)


    def get_logistics_emissions(self):
        """
        Calculates electricity use for biomass drying and VOC emissions from
        wood drying

        Electricity:
        Tally electricity consumption from feedstock processing
        Update logistics table with these values

        Equation for computing electricity consumption (generated by Ethan
        Warner):

        E = B * electricity_per_dt

        E = electricity (kWh per year per county)
        B = biomass production (dry short ton per yr per county)
        electricity_per_dt = electricity consumed (kWh per dry short ton?

        VOC emissions:
        Compute VOC emissions from wood drying
        Only applies to forestry

        Equation for computing VOC emissions from wood drying (generated
        by Ethan Warner):

        VOC = (B * a) * (VOC_ef_hammermill + VOC_ef_dryer) / b

        VOC = VOC emissions (metric tons per year per county)
        B = biomass production (dry short ton per yr per county)
        a = constant (0.9071847 metric tons per short ton)
        VOC_ef_h = emission factor for VOC from hammer mill (kg per dry
        metric ton of feedstock)
        VOC_ef_d = emission factor for VOC from grain dryer (kg per dry
        metric ton of feedstock)
        b = constant (1000 kg per metric ton)

        :return: output_df containing electricity consumption for biomass
        drying by feedstock and FIPS, and VOC emissions from wood drying (
        residues and whole trees only) also by feedstock and FIPS
        """
        output_df = self.transport.merge(self.electricity_per_dt,
                                         on = ['feed_id',
                                               'logistics_type'],
                                         how = 'left').merge(
            self.voc_wood_ef, on = ['feed_id', 'logistics_type'], how = 'left')

        # add column containing VOC emissions from wood drying
        # 0.9071847: metric ton per short ton
        # 1000.0: kg per metric ton
        output_df['voc'] = output_df['used_qnty'] * \
                           (output_df['grain_dryer_ef'] +
                            output_df['hammer_mill_ef']) * (0.9071847/1000.0)

        # add column containing electricity use for biomass drying
        output_df['electricity'] = output_df['used_qnty'] * \
                                   output_df['kWh_per_dt']

        # add column defining source category and logistics type
        output_df['source_category'] = 'Pre-processing, '\
                                       + output_df['logistics_type']

        return output_df
