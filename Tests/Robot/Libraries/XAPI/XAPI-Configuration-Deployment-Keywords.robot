*** Variables ***

*** Settings ***


Library     common/Xapi.py
Library     common/Cli.py
Library     common/Utils.py


Variables   Environments/Config/waits.yaml



*** Keywords ***
#####  Config Push to Devices  #####
xapi push config
    [Documentation]  Push Config to a Single Device(s) - AH-AP
    [Arguments]  ${DEVICE_ID}

    ${RESP}=  rest api post      /deployments      post_data='{"devices": {"ids": [ ${DEVICE_ID}]},"policy": {"enable_complete_configuration_update": false,"firmware_upgrade_policy": {"enable_distributed_upgrade": false,"enable_enforce_upgrade": false},"firmware_activate_option": {"enable_activate_at_next_reboot": true,"activation_delay_seconds": 0,"activation_time": 0}}}'        result_code=200
    log                             ${RESP}
    [Return]                        ${RESP}
	
	
xapi configuration push deployment status
    [Documentation]  Get Push Configuration Deployment Status of a Device
    [Arguments]  ${DEVICE_ID}

    ${RESP}=  rest api get      /deployments/status?deviceIds=${DEVICE_ID}
    Log     ${RESP}
    ${DATA_ARRAY}=   get json values         ${RESP}            key=${DEVICE_ID}
    log     ${DATA_ARRAY}
    ${DEPLOYMENT_STATUS}=       get json values     ${DATA_ARRAY}       key=finished
    log  ${DEPLOYMENT_STATUS}
    [Return]    ${DEPLOYMENT_STATUS}

xapi push delta config
    [Documentation]  Push delta config to a Single Device(s) - AH-AP
    [Arguments]  ${DEVICE_ID}

    ${DATA_DELTA_CONFIG}=  set variable  '{"devices": {"ids": [${DEVICE_ID}]},"policy": {"enable_complete_configuration_update": false}}'
    ${RESP}=  rest api post  /deployments   post_data=${DATA_DELTA_CONFIG}  result_code=200
    log          ${RESP}
    [Return]     ${RESP}

xapi push complete config
    [Documentation]  Push complete config to a Single Device(s) - AH-AP
    [Arguments]  ${DEVICE_ID}

    ${DATA_COMPLETE_CONFIG_ONLY}=  set variable  '{"devices": {"ids": [${DEVICE_ID}]},"policy": {"enable_complete_configuration_update": true, "firmware_activate_option": {"enable_activate_at_next_reboot": false,"activation_delay_seconds": 10, "activation_time": 0}}}'
    ${RESP}=  rest api post  /deployments   post_data=${DATA_COMPLETE_CONFIG_ONLY}  result_code=200
    log          ${RESP}
    [Return]     ${RESP}

xapi push complete config and firmware
    [Documentation]  Push complete config and firmware to a Single Device(s) - AH-AP
    [Arguments]  ${DEVICE_ID}

    ${DATA_COMPLETE_CONFIG_AND_FW}=  set variable  '{"devices": {"ids": [${DEVICE_ID}]},"policy": {"enable_complete_configuration_update": true, "firmware_upgrade_policy": {"enable_distributed_upgrade": false,"enable_enforce_upgrade": true}, "firmware_activate_option": {"enable_activate_at_next_reboot": false,"activation_delay_seconds": 10,"activation_time": 0}}}'
    ${RESP}=  rest api post  /deployments   post_data=${DATA_COMPLETE_CONFIG_AND_FW}  result_code=200
    log          ${RESP}
    [Return]     ${RESP}