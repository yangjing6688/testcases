*** Settings ***


Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py

Variables   Environments/Config/waits.yaml


*** Keywords ***
#####  Get Root Location  #####
xapi get root location id
    [Documentation]  Get Root Location ID

    #${RESP}=  rest api get      /locations/tree
    ${RESP}=  rest api get      /locations/tree?expandChildren=false
    Log     ${RESP}
    ${ROOT_LOCATION_ID}=   get json values         ${RESP}            index=0,key=id
    log  ${ROOT_LOCATION_ID}
    [Return]    ${ROOT_LOCATION_ID}
	

	
#####  Create Location  #####
xapi create location
    [Documentation]  Used to Create a Location
    [Arguments]      ${PARENT_ID}   ${LOCATION_NAME}
    ${RESPONSE}=     rest api post v3        /locations          '{ "parent_id": "${PARENT_ID}", "name": "${LOCATION_NAME}" }'       result_code=202
    Log              ${RESPONSE}
    ${LOCATION_ID}=  get json values         ${RESPONSE}            key=id
    Log              ${LOCATION_ID}
    [Return]         ${LOCATION_ID}	
	
	
    
xapi delete location
    [Documentation]   Used to Delete LOCATION by ID
    [Arguments]       ${LOCATION_ID}
    #${RESPONSE}=      rest api delete      /locations/${LOCATION_ID}
    ${RESPONSE}=      rest api v3        /locations/${LOCATION_ID}         operation=DELETE
    sleep  5
    Log               ${RESPONSE}
    [Return]          ${RESPONSE}

xapi create building
    [Documentation]  Used to Create the Building
    [Arguments]      ${PARENT_ID}   ${BUILDING_NAME}    ${BUILDING_ADDRESS}
    ${RESPONSE}=     rest api post v3       /locations/building          '{ "parent_id": "${PARENT_ID}", "name": "${BUILDING_NAME}", "address": "${BUILDING_ADDRESS}"}'       result_code=202
    Log              ${RESPONSE}
    ${BUILDING_ID}=  get json values         ${RESPONSE}            key=id
    Log              ${BUILDING_ID}
    [Return]         ${BUILDING_ID}



xapi delete building
    [Documentation]   TC-6766: Topology-Delete BUILDING by ID
    [Arguments]       ${BUILDING_ID}
    #${BUILDING_DELETE_RESP}=                 rest api delete      /locations/building/${BUILDING_ID}
    ${BUILDING_DELETE_RESP}=      rest api v3        /locations/building/${BUILDING_ID}         operation=DELETE
    Log               ${BUILDING_DELETE_RESP}
    sleep  5
    [Return]          ${BUILDING_DELETE_RESP}

    

xapi create floor
    [Documentation]  Used to Create the Floor
    [Arguments]      ${PARENT_ID}   ${FLOOR_NAME}
    ${RESPONSE}=     rest api post v3     /locations/floor        '{"parent_id": "${PARENT_ID}", "name": "${FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": ""}'   result_code=202
    Log              ${RESPONSE}
    ${FLOOR_ID}=     get json values         ${RESPONSE}            key=id
    Log              ${FLOOR_ID}
    [Return]         ${FLOOR_ID}



xapi delete floor
    [Documentation]   Used to Delete FLOOR by ID
    [Arguments]       ${FLOOR_ID}
    #${FLOOR_DELETE_RESP}=      rest api delete      /locations/floor/${FLOOR_ID}
    ${FLOOR_DELETE_RESP}=      rest api v3        /locations/floor/${FLOOR_ID}         operation=DELETE
    sleep  5
    Log               ${FLOOR_DELETE_RESP}
    [Return]          ${FLOOR_DELETE_RESP}


    
    
xapi assign location to device
    [Documentation]  Used to Assign Location To A Device
    [Arguments]      ${DEVICE_ID}   ${FLOOR_ID}

    ${RESPONSE}=            rest api put v3        /devices/${DEVICE_ID}/location         '{ "location_id": ${FLOOR_ID}, "x": 0, "y": 0, "latitude": 0, "longitude": 0 }'
    Log                     ${RESPONSE}
    [Return]         ${RESPONSE}
	

#xapi assign location to device
#    [Documentation]  Used to Assign Location To A Device
#    [Arguments]      ${SERIAL_NUMBER}   ${LOCATION_ID}
#    ${DEVICE_ID}=           Get Device Id With SerialNumber     ${SERIAL_NUMBER}
#    ${RESPONSE}=            rest api put        /devices/${DEVICE_ID}/location         '{ "location_id": ${LOCATION_ID}, "x": 0, "y": 0, "latitude": 0, "longitude": 0 }'
#    Log                     ${RESPONSE}
#    should be equal as integers             ${RESPONSE}         1

xapi get locations tree string
    [Documentation]  Used to Get the Locations Tree as String
    ${LOCATIONS_TREE}=          rest api get             /locations/tree
    Log                         ${LOCATIONS_TREE}
    ${LOCATIONS_TREE_STRING}=   get json value as string  ${LOCATIONS_TREE}
    log                         ${LOCATIONS_TREE_STRING}
    [Return]                    ${LOCATIONS_TREE_STRING}
    

    
    
##################################







xapi create location with no parent id
    [Documentation]  Used to Create a Location without Parent Id
    [Arguments]      ${LOCATION_NAME}
    #${RESPONSE}=     rest api post        /locations          '{ "name": "${LOCATION_NAME}" }'       result_code=202
    #${STATUS}  ${RESPONSE}=     rest api post v2        /locations          '{ "name": "${LOCATION_NAME}" }'       result_code=202
    ${RESPONSE}=     rest api post v3        /locations          '{ "name": "${LOCATION_NAME}" }'       result_code=202
    Log		     ${RESPONSE}
    #Log              ${STATUS}
    [Return]         ${RESPONSE}


xapi create location with no name
    [Documentation]  Used to Create a Location with No Name
    [Arguments]      ${PARENT_ID}
    #${RESPONSE}=     rest api post        /locations          '{ "parent_id": "${PARENT_ID}" }'       result_code=202
    ${RESPONSE}=     rest api post v3        /locations          '{ "parent_id": "${PARENT_ID}" }'       result_code=202
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}


xapi update location and get api response
    [Documentation]  Used to Update a Location And Get API Response
    [Arguments]      ${PARENT_ID}   ${LOCATION_ID}    ${NEW_LOCATION_NAME}
    ${RESPONSE}=     rest api put v3      /locations/${LOCATION_ID}         '{ "parent_id": "${PARENT_ID}", "name": "${NEW_LOCATION_NAME}" }'
    Log               ${RESPONSE}
    [Return]         ${RESPONSE}

xapi update location and get api response with status
    [Documentation]  Used to Update a Location And Get API Response
    [Arguments]      ${PARENT_ID}   ${LOCATION_ID}    ${NEW_LOCATION_NAME}
    ${httpCode}  ${RESPONSE}=     rest api put      /locations/${LOCATION_ID}         '{ "parent_id": "${PARENT_ID}", "name": "${NEW_LOCATION_NAME}" }'      result_code=response_map
    Log               ${httpCode}
    Log               ${RESPONSE}
    [Return]         ${RESPONSE}

xapi update location
    [Documentation]  Used to Update a Location
    [Arguments]      ${PARENT_ID}   ${LOCATION_ID}    ${NEW_LOCATION_NAME}
    ${RESPONSE}=     xapi update location and get api response      ${PARENT_ID}   ${LOCATION_ID}    ${NEW_LOCATION_NAME}
    Log              ${RESPONSE}
    #should be equal as integers             ${RESPONSE}         1
    #should be equal as numbers             ${RESPONSE}         1.0
    [Return]              ${LOCATION_ID}



xapi create building with no parent id
    [Documentation]  Used to Create a Building without Parent Id
    [Arguments]      ${BUILDING_NAME}
    #${RESPONSE}=     rest api post        /locations/building          '{ "name": "${BUILDING_NAME}", "address": "${BUILDING_NAME}"}'       result_code=202
    ${RESPONSE}=     rest api post v3        /locations/building          '{ "name": "${BUILDING_NAME}", "address": "${BUILDING_NAME}"}'       result_code=202
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}

xapi create building with no name and address
    [Documentation]  Used to Create a Building With No Name And Address
    [Arguments]      ${PARENT_ID}
    #${RESPONSE}=     rest api post        /locations/building          '{ "parent_id": "${PARENT_ID}"}'       result_code=202
    ${RESPONSE}=     rest api post v3        /locations/building          '{ "parent_id": "${PARENT_ID}"}'       result_code=202
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}


xapi update building and get api response
    [Documentation]  Used to Update a Building And Get API Response
    [Arguments]      ${PARENT_ID}   ${BUILDING_ID}    ${NEW_BUILDING_NAME}
    ${RESPONSE}=     rest api put v3     /locations/building/${BUILDING_ID}         '{ "parent_id": "${PARENT_ID}", "name": "${NEW_BUILDING_NAME}", "address": "${NEW_BUILDING_NAME}"}'
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}

xapi update building and get api response with status
    [Documentation]  Used to Update a Building And Get API Response
    [Arguments]      ${PARENT_ID}   ${BUILDING_ID}    ${NEW_BUILDING_NAME}
    ${httpCode}  ${RESPONSE}=     rest api put     /locations/building/${BUILDING_ID}         '{ "parent_id": "${PARENT_ID}", "name": "${NEW_BUILDING_NAME}", "address": "${NEW_BUILDING_NAME}"}'      result_code=response_map
    Log              ${httpCode}
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}


xapi update building
    [Documentation]  Used to Update a Building
    [Arguments]      ${PARENT_ID}   ${BUILDING_ID}    ${NEW_BUILDING_NAME}
    ${RESPONSE}=     xapi update building and get api response      ${PARENT_ID}   ${BUILDING_ID}    ${NEW_BUILDING_NAME}
    #should be equal as integers             ${RESPONSE}         1
    #should be equal as numbers             ${RESPONSE}         1.0
    [Return]         ${BUILDING_ID}


xapi create floor with no parent id
    [Documentation]  Used to Create the Floor With No Parent Id
    [Arguments]      ${FLOOR_NAME}
    #${RESPONSE}=     rest api post     /locations/floor        '{"name": "${FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'   result_code=202
    ${RESPONSE}=     rest api post v3     /locations/floor        '{"name": "${FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'   result_code=202
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}


xapi create floor with no name
    [Documentation]  Used to Create the Floor With No Name
    [Arguments]      ${PARENT_ID}
    #${RESPONSE}=     rest api post     /locations/floor        '{"parent_id": "${PARENT_ID}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'   result_code=202
    ${RESPONSE}=     rest api post v3     /locations/floor        '{"parent_id": "${PARENT_ID}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'   result_code=202
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}


xapi update floor and get api response
    [Documentation]  Used to Update a Floor And Get API Response
    [Arguments]      ${PARENT_ID}   ${FLOOR_ID}    ${NEW_FLOOR_NAME}
     ${RESPONSE}=     rest api put v3      /locations/floor/${FLOOR_ID}         '{"parent_id": "${PARENT_ID}", "name": "${NEW_FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'
     Log              ${RESPONSE}
     [Return]         ${RESPONSE}

xapi update floor and get api response with status
    [Documentation]  Used to Update a Floor And Get API Response
    [Arguments]      ${PARENT_ID}   ${FLOOR_ID}    ${NEW_FLOOR_NAME}
    #${RESPONSE}=     rest api put v3      /locations/floor/${FLOOR_ID}         '{"parent_id": "${PARENT_ID}", "name": "${NEW_FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'
    ${httpCode}  ${RESPONSE}=     rest api put      /locations/floor/${FLOOR_ID}         '{"parent_id": "${PARENT_ID}", "name": "${NEW_FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "15", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'      result_code=response_map
    Log              ${httpCode}
    Log              ${RESPONSE}
    [Return]         ${RESPONSE}

xapi update floor
    [Documentation]  Used to Update a Floor
    [Arguments]      ${PARENT_ID}   ${FLOOR_ID}    ${NEW_FLOOR_NAME}
    ${RESPONSE}=     xapi update floor and get api response      ${PARENT_ID}   ${FLOOR_ID}    ${NEW_FLOOR_NAME}
    #should be equal as integers             ${RESPONSE}         1
    #should be equal as numbers             ${RESPONSE}         1.0
    [Return]         ${FLOOR_ID}


xapi create floor with incorrect db attenuation
    [Documentation]  Used to Create the Floor With Incorrect DB Attenuation
    [Arguments]      ${PARENT_ID}   ${FLOOR_NAME}
    #${RESPONSE}=     rest api post     /locations/floor        '{"parent_id": "${PARENT_ID}", "name": "${FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "SHOULD_BE_DOUBLE", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'   result_code=202
    ${RESPONSE}=     rest api post v3     /locations/floor        '{"parent_id": "${PARENT_ID}", "name": "${FLOOR_NAME}", "environment": "AUTO_ESTIMATE", "db_attenuation": "SHOULD_BE_DOUBLE", "measurement_unit": "FEET", "installation_height": "12", "map_size_width": "12", "map_size_height": "12", "map_name": "" }'   result_code=202
    Log              ${RESPONSE}
    ${FLOOR_ID}=     get json values         ${RESPONSE}            key=id
    Log              ${FLOOR_ID}
    [Return]         ${FLOOR_ID}


xapi upload floor plan
    [Documentation]   Used to Upload Floor Plan
    [Arguments]       ${FLOOR_PLAN_IMAGE}
    ${RESPONSE}=      rest api post with file          /locations/floorplan          ${FLOOR_PLAN_IMAGE}
    Log               ${RESPONSE}
    [Return]          ${RESPONSE}


xapi upload floor plan get response string
    [Documentation]   Used to Upload Floor Plan
    [Arguments]       ${FLOOR_PLAN_IMAGE}
    ${RESPONSE}=            xapi upload floor plan           ${FLOOR_PLAN_IMAGE}
    ${RESPONSE_STRING}=     get json value as string    ${RESPONSE}
    [Return]                ${RESPONSE_STRING}


xapi upload floor plan with no image
    [Documentation]   Used to Upload Floor Plan With No Image
    ${RESPONSE}=            rest api post with no file          /locations/floorplan
    ${RESPONSE_STRING}=     get json value as string            ${RESPONSE}
    [Return]                ${RESPONSE_STRING}
    

