*** Variables ***

${index_value}=    0

*** Settings ***

Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py


Variables   Environments/Config/waits.yaml


*** Keywords ***

xapi ap device onboard
    [Documentation]  Onboard Single AH-AP Device
    [Arguments]  ${AP_SERIAL_NUMBER}

    ${RESP}=  rest api post      /devices/:onboard      post_data='{"extreme": {"sns": ["${AP_SERIAL_NUMBER}"]}}'        result_code=202
    log                             ${RESP}
    [Return]                        ${RESP}

xapi extreme switch onboard
    [Documentation]  Onboard Single Extreme SR Switch Device
    [Arguments]  ${SW_SERIAL_NUMBER}

    ${RESP}=  rest api post      /devices/:onboard      post_data='{"extreme": {"sns": ["${SW_SERIAL_NUMBER}"]}}'        result_code=202
    log                             ${RESP}
    [Return]                        ${RESP}

xapi onboard multiple extreme devices
    [Documentation]  Onboard Multiple devices
    [Arguments]  ${SERIAL_NUMBER_1}    ${SERIAL_NUMBER_2}

    ${RESP}=  rest api post      /devices/:onboard      post_data='{"extreme": {"sns": ["${SERIAL_NUMBER_1}, ${SERIAL_NUMBER_2}"]}}'        result_code=202
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


xapi wait until device online
    [Documentation]  Wait till the device is connected
    [Arguments]  ${SERIAL_NUMBER}   ${RETRY_COUNT}      ${RETRY_DURATION}

    FOR    ${i}    IN RANGE    ${RETRY_COUNT}
        ${DEVICE_CONNECTED_STATE}=                  xapi list device connected status         ${SERIAL_NUMBER}
        Log      ${DEVICE_CONNECTED_STATE}
        Exit For Loop If   '${DEVICE_CONNECTED_STATE}'=='True'
        Log      ${i}
        sleep    ${RETRY_DURATION}

    END
    Log     ${DEVICE_CONNECTED_STATE}
    Log    Exiting as Device is Conneceted
    [Return]    ${DEVICE_CONNECTED_STATE}
