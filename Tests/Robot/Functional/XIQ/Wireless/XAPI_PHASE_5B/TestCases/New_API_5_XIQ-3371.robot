# Author        : Subramani R
# Date          : 24 March 2022
# Description   : XAPI - Reset a device to factory defaults

# Topology:
# ---------
#    ScriptHost
#      |________
#      |        |
#     Cloud     AP
# Pre-config:
# -----------
#
#

# Execution Command:
# ------------------
# robot  -v TOPO:topo.xapi.phase5b.yaml New_API_5_XIQ-3371.robot
#
#


*** Variables ***
# Provide random index value as below when there are multiple devices

${DEVICE_ID}=   0
${INDEX_VALUE}=   0
${DEVICE_RESET_URI}=  /devices/{DEVICE_ID}/:reset
${LIST_DEVICES_URI}=  /devices
${ERROR_CODE}=  error_code




*** Settings ***
Force Tags  testbed_1_node

Library     common/TestFlow.py
Library     common/Xapi.py
Library     common/Utils.py
Library     xiq/flows/common/Login.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/configure/CommonObjects.py

Resource    ../../XAPI_PHASE_5A/Resources/AllResources.robot

Variables   Environments/Config/waits.yaml

*** Keywords ***

list and get device id
    [Documentation]  List Devices and Get Device ID
    #[Arguments]  ${INDEX_VALUE}

    ${RESP}=  rest api get  ${LIST_DEVICES_URI}
    ${DATA}=  get json values       ${RESP}         key=data
    log     ${DATA}

    ${ID}=  get index id from list json   ${DATA}     ${INDEX_VALUE}
    log  ${ID}
    [Return]  ${ID}

reset device
    [Documentation]  Reset a device to factory default settings
    [Arguments]  ${DEVICE_ID}

    ${RESP}=     rest api post    /devices/${DEVICE_ID}/:reset      result_code=200
    log  ${RESP}
    [Return]  ${RESP}


*** Test Cases ***

# generate the key once per suite
Pre Condition-Login
    [Documentation]         Login and generate access_token
    [Tags]                  xim_tcxm_16480     development

    ${ACCESS_TOKEN}=        generate_access_token    ${tenant_username}      ${tenant_password}      login
    set global variable     ${ACCESS_TOKEN}

Pre Condition-Get Device ID
    [Documentation]         List and Get Device ID
    [Tags]                  xim_tcxm_9437     development

    ${DEVICE_ID}=        list and get device id
    set global variable     ${DEVICE_ID}

TCXM-18243: Reset Device
    [Documentation]         reset device
    [Tags]                  xim_tcxm_18243    xim_tcxm_18244       development

    ${RESP}=  reset device    ${DEVICE_ID}
    ${RESPONSE_STRING}=       get json value as string          ${RESP}
    should not contain     ${RESPONSE_STRING}      ${ERROR_CODE}
