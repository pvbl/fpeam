import os, tempfile

#Create Run config file
def runConfigCreation(tmpFolder, attributeValueObj):

    ini_template_string = """[run_config]
## run identifier
scenario_name = '{scenario_name}'
    
## project output directory
project_path = '{project_path}'

## modules to run
modules = {modules}

## logging verbosity level (CRITICAL, ERROR, WARNING, INFO, DEBUG, UNSET)
logger_level = {logger_level}

## data paths
equipment = '{equipment}'
production = '{production}'
feedstock_loss_factors = '{feedstock_loss_factors}'

## forest feedstocks have different allocation indicators in NONROAD and onroad fugitive dust calculations
forestry_feedstock_names = '{forestry_feedstock_names}'

## MOVES routing graph
transportation_graph = '{transportation_graph}'

## truck capacities for feedstock transportation
truck_capacity = '{truck_capacity}'

## data backfill flag
backfill = {backfill}

## use the router engine to calculate vmt by county
use_router_engine = {use_router_engine} """

    # convert the forestry feedstock name input into a list
    if attributeValueObj.forestry_feedstock_names.__contains__(','):
        _forestry_feedstock_names_list = attributeValueObj.forestry_feedstock_names.split(',')
    elif attributeValueObj.forestry_feedstock_names.__contains__(';'):
        _forestry_feedstock_names_list = attributeValueObj.forestry_feedstock_names.split(';')
    else:
        _forestry_feedstock_names_list = attributeValueObj.forestry_feedstock_names


    my_ini_config = ini_template_string.format(scenario_name=attributeValueObj.scenarioName,
                                               project_path=attributeValueObj.projectPath,
                                               modules = attributeValueObj.module ,
                                               logger_level = attributeValueObj.loggerLevel ,
                                               equipment = attributeValueObj.equipment,
                                               production = attributeValueObj.production,
                                               feedstock_loss_factors = attributeValueObj.feedstockLossFactors,
                                               forestry_feedstock_names=_forestry_feedstock_names_list,
                                               transportation_graph = attributeValueObj.transportationGraph,
                                               truck_capacity=attributeValueObj.truckCapacity,
                                               backfill = attributeValueObj.backfill,
                                               use_router_engine = attributeValueObj.useRouterEngine)


    my_ini_file_path = os.path.join(tmpFolder,"run_config.ini")
    with open(my_ini_file_path, 'w') as f:
        f.write(my_ini_config)

    return my_ini_file_path