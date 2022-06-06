*** Settings ***


Library     common/Xapi.py
Library     common/Cli.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/common/Navigator.py
Library     xiq/flows/extreme_location/ExtremeLocation.py
Library     xiq/flows/globalsettings/GlobalSetting.py
Library     xiq/flows/configure/AdditionalSettings.py

Library     common/TestFlow.py
Library     common/Utils.py

Library     xiq/flows/manage/Devices.py
Library     Collections


#Resource    ../../XAPI_PHASE_5A/Resources/AllResources.robot
#Resource    Tests/Robot/Libraries/XIQ/Wireless/XAPI/XAPI-Production-Sanity-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}
#Variables   Environments/${ENV}


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
    ${RESPONSE}=      rest api delete      /locations/${LOCATION_ID}
    sleep  5
    Log               ${RESPONSE}


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
    ${BUILDING_DELETE_RESP}=                 rest api delete      /locations/building/${BUILDING_ID}
    Log               ${BUILDING_DELETE_RESP}
    sleep  5


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
    ${FLOOR_DELETE_RESP}=      rest api delete      /locations/floor/${FLOOR_ID}
    sleep  5
    Log               ${FLOOR_DELETE_RESP}


xapi assign location to device
    [Documentation]  Used to Assign Location To A Device
    [Arguments]      ${DEVICE_ID}   ${FLOOR_ID}

    ${RESPONSE}=            rest api put v3        /devices/${DEVICE_ID}/location         '{ "location_id": ${FLOOR_ID}, "x": 0, "y": 0, "latitude": 0, "longitude": 0 }'
    Log                     ${RESPONSE}
	[Return]         ${RESPONSE}

xapi get locations tree string
    [Documentation]  Used to Get the Locations Tree as String
    ${LOCATIONS_TREE}=          rest api get             /locations/tree
    Log                         ${LOCATIONS_TREE}
    ${LOCATIONS_TREE_STRING}=   get json value as string  ${LOCATIONS_TREE}
    log                         ${LOCATIONS_TREE_STRING}
    [Return]                    ${LOCATIONS_TREE_STRING}