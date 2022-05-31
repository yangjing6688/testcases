*** Variables ***

${index_value}=    0

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


*** Keywords ***

xapi device onboard
    [Documentation]  Onboard Single device
    [Arguments]  ${AP_SERIAL_NUMBER}

    ${RESP}=  rest api post      /devices/:onboard      post_data='{"extreme": {"sns": ["${AP_SERIAL_NUMBER}"]}}'        result_code=202
    log                             ${RESP}
    [Return]                        ${RESP}

xapi onboard multiple devices
    [Documentation]  Onboard Multiple devices
    [Arguments]  ${AP1_SERIAL_NUMBER}    ${AP2_SERIAL_NUMBER}

    ${RESP}=  rest api post      /devices/:onboard      post_data='{"extreme": {"sns": ["${AP1_SERIAL_NUMBER}, ${AP2_SERIAL_NUMBER}"]}}'        result_code=202
    log                             ${RESP}
    [Return]                        ${RESP}


xapi list and get device id
    [Documentation]  List Devices and Get Device ID
    [Arguments]  ${SERIAL_NUMBER}

    ${RESP}=  rest api get      /devices?sns=${SERIAL_NUMBER}
    Log     ${RESP}
    ${DATA_ARRAY}=  get json values      ${RESP}     key=data
    Log     ${DATA_ARRAY}
    ${DEVICE_ID}=   get index id from list json   ${DATA_ARRAY}     ${index_value}
    log  ${DEVICE_ID}
    [Return]    ${DEVICE_ID}


xapi list device connected status
    [Documentation]  Get Device Connected Status
    [Arguments]  ${SERIAL_NUMBER}

    ${RESP}=  rest api get      /devices?sns=${SERIAL_NUMBER}
    Log     ${RESP}
    ${DATA_ARRAY}=  get json values      ${RESP}     key=data
    Log     ${DATA_ARRAY}

    ${DEVICE_CONNECTED_STATE}=  get index connected status from list json      ${DATA_ARRAY}     ${index_value}
    Log     ${DEVICE_CONNECTED_STATE}

    [Return]    ${DEVICE_CONNECTED_STATE}

xapi list device admin state
    [Documentation]  Get Device Admin State
    [Arguments]  ${SERIAL_NUMBER}

    ${RESP}=  rest api get      /devices?sns=${SERIAL_NUMBER}
    Log     ${RESP}
    ${DATA_ARRAY}=  get json values      ${RESP}     key=data
    Log     ${DATA_ARRAY}
    ${DEVICE_ADMIN_STATE}=  get index device admin state from list json      ${DATA_ARRAY}     ${index_value}
    Log     ${DEVICE_ADMIN_STATE}
    [Return]    ${DEVICE_ADMIN_STATE}


xapi reset device
    [Documentation]  Reset a device to factory default settings
    [Arguments]  ${DEVICE_ID}

    ${RESP}=     rest api post    /devices/${DEVICE_ID}/:reset      result_code=200
    log  ${RESP}
    [Return]  ${RESP}

xapi delete device
    [Documentation]  delete a single device
    [Arguments]  ${DEVICE_ID}
    ${RESP}=  rest api delete  /devices/${DEVICE_ID}
    log  ${RESP}
    [Return]  ${RESP}

xapi delete multiple devices
    [Documentation]  delete devices
    [Arguments]  ${AP_DEVICE_ID}    ${SWITCH_DEVICE_ID}
    ${RESP}=  rest api post  /devices/:delete     '{"ids": [${AP_DEVICE_ID}, ${SWITCH_DEVICE_ID}]}'
    log  ${RESP}
    [Return]  ${RESP}


xapi list device network policy name
    [Documentation]  Get Network Policy Name for a device
    [Arguments]  ${SERIAL_NUMBER}

    ${RESP}=  rest api get      /devices?views=FULL&sns=${SERIAL_NUMBER}
    Log     ${RESP}
    ${DATA_ARRAY}=  get json values      ${RESP}     key=data
    Log     ${DATA_ARRAY}
    ${DEVICE_NW_POLICY_NAME}=  get index nw policy name from list json      ${DATA_ARRAY}     ${index_value}
    Log     ${DEVICE_NW_POLICY_NAME}
    [Return]    ${DEVICE_NW_POLICY_NAME}
