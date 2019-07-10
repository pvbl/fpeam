import os, tempfile


def nonroadConfigCreation(tmpFolder, attributeValueObj):

    ini_template_string = """ [nonroad]
    
    ## start year (equipment year #1)
    #year = {year}    
    
    ### input data options
    
    ## production table row identifier (feedstock_measure in production data)
    #feedstock_measure_type = '{feedstock_measure_type}'
    
    ## equipment table row identifier (resource in equipment data)
    #time_resource_name = '{time_resource_name}'
    
    ## forest feedstocks have different allocation indicators
    #forestry_feedstock_names = '{forestry_feedstock_names}'
    
    
    ### input data files
    
    ## production region to NONROAD FIPS mapping
    #region_fips_map = '{region_fips_map}'
    
    #nonroad_datafiles_path = '{nonroad_datafiles_path}'
    
    ### NONROAD input options
    
    # temperature range
    #nonroad_temp_min = {nonroad_temp_min}
    #nonroad_temp_max = {nonroad_temp_max}
    #nonroad_temp_mean = {nonroad_temp_mean}
    
    ## lower heating value for diesel fuel (mmBTU/gallon)
    #diesel_lhv = {diesel_lhv}
    
    # nh3 emission factor for diesel fuel (grams NH3/mmBTU diesel)
    #diesel_nh3_ef = {diesel_nh3_ef}
    
    ## VOC conversion factor
    #diesel_thc_voc_conversion = {diesel_thc_voc_conversion}
    
    ## pm10 to PM2.5 conversion factor
    #diesel_pm10topm25 ={diesel_pm10topm25}
     
     ## production table row identifier for irrigation activity calculation
    irrigation_feedstock_measure_type = '{irrigation_feedstock_measure_type}'
    
    ## list of irrigated feedstocks
    irrigated_feedstock_names = '{irrigated_feedstock_names}'
    
    ## irrigation dataset
    irrigation = '{irrigation}'
    
    # encode feedstock, tillage type and activity names
    encode_names = '{encode_names}'"""

    my_ini_config = ini_template_string.format(year = attributeValueObj.yearNonroad,
                                               feedstock_measure_type = attributeValueObj.feedMeasureTypeEF,
                                               time_resource_name = attributeValueObj.timeResourceNameNon,
                                               forestry_feedstock_names = attributeValueObj.forestryFeedstockNames,
                                               region_fips_map = attributeValueObj.regionFipsMapNonroad,
                                               nonroad_datafiles_path = attributeValueObj.nonroadDatafilesPath,
                                               nonroad_temp_min = attributeValueObj.tempMin,
                                               nonroad_temp_max = attributeValueObj.tempMax,
                                               nonroad_temp_mean = attributeValueObj.tempMean,
                                               diesel_lhv = attributeValueObj.dieselLHV,
                                               diesel_nh3_ef = attributeValueObj.dieselNh3Ef,
                                               diesel_thc_voc_conversion = attributeValueObj.dieselThcVocConversion,
                                               diesel_pm10topm25 = attributeValueObj.dieselPm10topm25,
                                               irrigation_feedstock_measure_type=attributeValueObj.irrigationFeedstockMeasureType,
                                               irrigated_feedstock_names = attributeValueObj.irrigatedFeedstockNames ,
                                               irrigation = attributeValueObj.irrigation,
                                               encode_names = attributeValueObj.encodeNames)


    print(tmpFolder)

    my_ini_file_path = os.path.join(tmpFolder, "nonroad.ini")
    with open(my_ini_file_path, 'w') as f:
        f.write(my_ini_config)

    return my_ini_file_path
    ##########################

    #
    # with open(my_ini_file_path) as f:
    #     print(my_ini_file_path)
    #     # print(f.read())
    #     pass
    #
    # os.system("fpim "+my_ini_file_path)
