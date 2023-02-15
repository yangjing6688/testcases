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

    #Kun Li: Fix the sns list issue
    ${RESP}=  rest api post   /devices/:onboard   post_data='{"extreme": {"sns": ["${SERIAL_NUMBER_1}", "${SERIAL_NUMBER_2}"]}}'  result_code=202
    log       ${RESP}
    [Return]  ${RESP}

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


xapi Get iBeacon Settings
    [Documentation]     get iBeacon settings by device id
    [Arguments]         ${ID}
    log                 get device iBeacon URL : /devices/${ID}/ibeacon
    ${RESP} =           rest api get     /devices/${ID}/ibeacon
    log                 get device iBeacon resp: ${RESP}
    [Return]            ${RESP}


xapi Update iBeacon Settings
    [Documentation]     update iBeacon settings by multiple device IDs
    [Arguments]         ${DATA}
    log                 update multiple iBeacon settings URL: /devices/ibeacon
    log                 update multiple iBeacon settings DATA: ${DATA}
    ${RESP} =           rest api put v1   /devices/ibeacon    ${DATA}
    log                 update multiple iBeacon settings resp: ${RESP}
    [Return]            ${RESP}


xapi Assign country code
    [Documentation]  assign country code
    [Arguments]  ${DEVICE_ID}   ${COUNTRY_CODE}
    log     assigning device:${DEVICE_ID} country code:${COUNTRY_CODE}
    ${RESP}=  rest api post     /devices/country-code/:assign    '{"devices": {"ids": [${DEVICE_ID}]}, "country_code": "${COUNTRY_CODE}"}'
    log  ${RESP}
    [Return]  ${RESP}

########### Device Description Keywords#############
#####  Get sample id from devices Keywords   #####
xapi get sample id from devices
    [Documentation]  get a sample device id from device list
    ${RESP}=  rest api get  ${LIST_DEVICES_URI}
    ${DATA}=  get json values  ${RESP}  key=data
    ${ID}=   get random id from list json  ${DATA}
    log  ${ID}
    [Return]  ${ID}

#####  Get device description Keywords   #####
xapi get device description
    [Documentation]  get device description
    [Arguments]  ${ID}
    ${RESP}=  rest api get  /devices/${ID}?views=full
    ${DESCRIPTION}=  get json values  ${RESP}  key=description
    log  ${DESCRIPTION}
    [Return]  ${DESCRIPTION}

#####  Change device description Keywords   #####
xapi change device description
    [Documentation]  change device description
    [Arguments]  ${ID}  ${DESCRIPTION}
    ${RESPCODE}=  rest api put v1  /devices/${ID}/description    ${DESCRIPTION}
    log  ${RESPCODE}
    [Return]  ${RESPCODE}

xapi get device hostname
    [Documentation]  get device name
    [Arguments]  ${DEVICE_ID}
    ${RESP}=  rest api get  /devices/${DEVICE_ID}?views=full
    ${HOSTNAME}=  get json values  ${RESP}  key=hostname
    log  ${HOSTNAME}
    [Return]  ${HOSTNAME}

xapi change device hostname
    [Documentation]  change device hostname
    [Arguments]  ${DEVICE_ID}  ${HOSTNAME}
    ${RESP}=  rest api put v3  /devices/${DEVICE_ID}/hostname?hostname=${HOSTNAME}
    log  ${RESP}
    [Return]  ${RESP}

xapi change single device to managed
    [Documentation]  change single device to managed
    [Arguments]  ${DEVICE_ID}

    ${RESP}=  rest api post  /devices/${DEVICE_ID}/:manage
    log    ${RESP}
    [Return]   ${RESP}

xapi change multiple devices to managed
    [Documentation]  change multiple devices to managed
    [Arguments]  ${DEVICE1_ID}  ${DEVICE2_ID}

    ${RESP}=  rest api post  /devices/:manage  post_data='{"ids": [${DEVICE1_ID}, ${DEVICE2_ID}]}'
    log    ${RESP}
    [Return]   ${RESP}

xapi change single device to unmanaged
    [Documentation]  change single device to unmanaged
    [Arguments]  ${DEVICE_ID}

    ${RESP}=  rest api post  /devices/${DEVICE_ID}/:unmanage
    log    ${RESP}
    [Return]   ${RESP}

xapi change multiple devices to unmanaged
    [Documentation]  change multiple devices to unmanaged
    [Arguments]  ${DEVICE1_ID}  ${DEVICE2_ID}

    ${RESP}=  rest api post  /devices/:unmanage  post_data='{"ids": [${DEVICE1_ID}, ${DEVICE2_ID}]}'
    log    ${RESP}
    [Return]   ${RESP}

xapi reboot single device
    [Documentation]  reboot single device
    [Arguments]  ${DEVICE_ID}

    ${RESP}=  rest api post  /devices/${DEVICE_ID}/:reboot
    log    ${RESP}
    [Return]   ${RESP}

xapi reboot multiple devices
    [Documentation]  reboot multiple devices
    [Arguments]  ${DEVICE1_ID}  ${DEVICE2_ID}

    ${RESP}=  rest api post  /devices/:reboot  post_data='{"ids": ["${DEVICE1_ID}", "${DEVICE2_ID}"]}'
    log    ${RESP}
    [Return]   ${RESP}

xapi assign network policy to one device
    [Documentation]  assign network policy to single device
    [Arguments]  ${DEVICE_ID}  ${NETWORK_POLICY_ID}

    ${RESP}=  rest api put v1  /devices/${DEVICE_ID}/network-policy  ${NETWORK_POLICY_ID}
    log    ${RESP}
    [Return]   ${RESP}

xapi assign network policy to two devices
    [Documentation]  assign network policy to two devices
    [Arguments]  ${DEVICE1_ID}  ${DEVICE2_ID}  ${NETWORK_POLICY_ID}

    ${RESP}=  rest api post  /devices/network-policy/:assign  post_data='{"devices": {"ids": ["${DEVICE1_ID}", "${DEVICE2_ID}"]}, "network_policy_id": "${NETWORK_POLICY_ID}"}'
    log    ${RESP}
    [Return]   ${RESP}

xapi get device network policy id
    [Documentation]  get device network policy id
    [Arguments]  ${DEVICE_ID}

    ${DEV_NETWORK_POLICY_CONTENT}=  rest api get  /devices/${DEVICE_ID}/network-policy
    ${DEV_NETWORK_POLICY_ID}=  get json values  ${DEV_NETWORK_POLICY_CONTENT}  key=id
    [Return]    ${DEV_NETWORK_POLICY_ID}

xapi get device network policy name
    [Documentation]  xapi get device network policy name
    [Arguments]  ${DEVICE_ID}

    ${DEV_NETWORK_POLICY_CONTENT}=  rest api get  /devices/${DEVICE_ID}/network-policy
    ${DEV_NETWORK_POLICY_NAME}=  get json values  ${DEV_NETWORK_POLICY_CONTENT}  key=name
    [Return]    ${DEV_NETWORK_POLICY_NAME}