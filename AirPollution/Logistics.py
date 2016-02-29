# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 1:02:31 2016

Populates tables for logistics emissions and electricity consumption associated with feedstock processing

Inputs include: 
    list of feedstock types (feedstocklist)
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
    
    def __init__(self, feedstocklist, cont): 
        SaveDataHelper.SaveDataHelper.__init__(self, cont)
        # gets used to save query to a text file for debugging purposes.
        self.document_file = "Logistics"
        self.elec_per_dt = config.get('electric_dict')
        self.VOC_wooddrying_dict = config.get('VOC_wooddrying_dict')
        self.feedstocklist = feedstocklist
        self.production_schema = config.get('production_schema')
        self.logistics_type = config.get('logistics_type')
        self.scenario_name = config.get('title')
            
    def VOC_and_electric(self):
        """
        Compute VOC emissions from wood drying 
        and electricity consumption from feedstock processing
        """
        logger.info('Computing VOC emissions from wood drying')
        
        # equation for computing VOC emissions from wood drying (generated by Ethan Warner)
        # VOC = (B*a)*(VOC_ef)/b
        # 
        # VOC = VOC emissions (metric tons per year per county)
        # B = biomass production (dry short ton per yr per county)
        # a = constant (0.9071847 metric tons per short ton)
        # VOC_ef = emission factor for VOC (kg per dry metric ton of feedstock)
        # b = constant (1000 kg per metric ton)

        # equation for computing electricity consumption (generated by Ethan Warner)
        # E = B*elec_per_dt
        # E = electricity (kWh per year per county)
        # B = biomass production (dry short ton per yr per county)
        # elec_per_dt = electricity consumed (kWh per dry short ton 

        # initialize kvals for string formatting
        kvals = {}
        
        # set constants a and b
        kvals['a'] = 0.9071847
        kvals['b'] = 1000
        kvals['production_schema'] = self.production_schema
        kvals['scenario_name'] = self.scenario_name
        
        # initialize queries
        queries = ''
        
        for feed in self.feedstocklist: 
            # set column for production data
            kvals['column'] = 'prod'
            if feed == 'FR':
                kvals['column'] = 'fed_minus_55'
            if feed == 'CG':
                kvals['column'] = 'total_prod'
                
            # set VOC emission factor 
            kvals['VOC_ef'] = self.VOC_wooddrying_dict[feed][self.logistics_type]
            kvals['elec_per_dt'] = self.elec_per_dt[feed][self.logistics_type]
            # set feedstock name 
            kvals['feed'] = feed
            # generate string for query and append to queries
            # @ TODO: change query to use new table for FIPS code associated with processing rather than production (these data need to be imported into the database first)
            queries = queries + ("""INSERT INTO {scenario_name}.{feed}_logistics
            SELECT feed.fips, 
            feed.{column}*{a}*{VOC_ef}/{b} AS "VOC",
            feed.{column}*{elec_per_dt} AS "electricity"
            FROM {production_schema}.{feed}_data feed
            GROUP BY feed.fips;""").format(**kvals)
        
        self._execute_query(queries)
    