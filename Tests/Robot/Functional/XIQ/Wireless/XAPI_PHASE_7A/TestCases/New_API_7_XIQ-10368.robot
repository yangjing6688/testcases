# Author        : Jerome Ly
# Date          : 11 Oct 2022
# Description   : XAPI Automation for XIQ-4651 - Configure Cloud Config Groups

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
# robot  -v TOPO:topo.test.cp1r1.yaml -v TESTBED:SJ/Dev/xiq_sj_tb_sample.yaml New_API_7_XIQ-10368.robot
#


*** Variables ***
${ERROR_CODE}                   error_code

${INVALID_ARGUMENT}             INVALID_ARGUMENT

${ERROR_CODE_PATTERN}           "error_code":"INVALID_ARGUMENT"

*** Settings ***
Force Tags  testbed_1_node

Library     common/Xapi.py
Library     common/Cli.py
Library     common/TestFlow.py
Library     common/Utils.py

Resource    Tests/Robot/Libraries/XAPI/XAPI-Authentication-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Configuration-Policy-Keywords.robot
Resource    Tests/Robot/Libraries/XAPI/XAPI-Device-Keywords.robot

Variables   Environments/Config/waits.yaml
Variables   TestBeds/${TESTBED}
Variables   Environments/${TOPO}


*** Keywords ***

##### Get Response Error Code #####
Get Response Code
    [Documentation]         get the response error code
    [Arguments]             ${RESP}
    ${Code}=                get json values  ${RESP}  key=${ERROR_CODE}
    log                     response error code -- ${Code}
    [Return]                ${Code}


*** Test Cases ***

Pre Condition
    [Tags]                      tcxm_16480    development
#Login and Generate Access Token
    ${ACCESS_TOKEN} =           xapi login    ${tenant_username}      ${tenant_password}
    should not be empty         ${ACCESS_TOKEN}
    set suite variable          ${ACCESS_TOKEN}

#Onboard the device and save the device Id
    ${DEVICE_ONBOARD}=          xapi ap device onboard      ${ap1.serial}
    Log                         device onboard status: ${DEVICE_ONBOARD}
    Should Be Equal As Integers          ${DEVICE_ONBOARD}       1
    sleep                       ${device_onboarding_wait}
    sleep                       ${device_onboarding_wait}

#Get Device ID
    ${DEVICE_ID}=               xapi list and get device id     ${ap1.serial}
    should be true              ${DEVICE_ID}>0
    set suite variable          ${DEVICE_ID}


# CCGS Test Cases
# ------------------------

TR-20185: create valid cloud control group
    [Documentation]         create valid cloud control group for one/multiple devices IDs
    [Tags]                  tcxm_20185   development
    Depends On              tcxm_16480
    ${RESP} =               xapi Create Cloud Control Group     {"name": "valid-ccg-ssid1", "description": "create valid cloud config group for ssid1", "device_ids": [${DEVICE_ID}]}
    ${CCG_ID} =             get json values     ${RESP}     key=id
    ${name} =               get json values     ${RESP}     key=name
    ${description} =        get json values     ${RESP}     key=description
    should be true          ${CCG_ID}>0
    should be equal as strings      '${name}'               'valid-ccg-ssid1'
    should be equal as strings      '${description}'        'create valid cloud config group for ssid1'
    set suite variable      ${CCG_ID}

TR-20187: create partial invalid cloud control group
    [Documentation]         create partial invalid cloud control group for one bad devices ID
    [Tags]                  tcxm_20187   development
    Depends On              tcxm_16480
    ${RESP} =               xapi Create Cloud Control Group     {"name": "partial-valid-ccg-ssid1", "description": "partial invalid cloud control group for ssid1", "device_ids": [${DEVICE_ID}, 0]}
    ${RESP_CODE} =          Get Response Code   ${RESP}
    should be equal as strings          '${RESP_CODE}'     '${INVALID_ARGUMENT}'

TR-20189: create invalid cloud control group
    [Documentation]         create invalid cloud control group for one bad devices ID
    [Tags]                  tcxm_20189   development
    Depends On              tcxm_16480
    ${RESP} =               xapi Create Cloud Control Group     {"name": "invalid-ccg-ssid1", "description": "invalid cloud control group for ssid1", "device_ids": [0]}
    ${RESP_CODE} =          Get Response Code   ${RESP}
    should be equal as strings          '${RESP_CODE}'     '${INVALID_ARGUMENT}'

TR-20182: get cloud control group
    [Documentation]         get cloud control group by Id
    [Tags]                  tcxm_20182    development
    Depends On              tcxm_20185
    ${RESP} =               xapi Get Cloud Control Group    ${CCG_ID}
    ${name} =               get json values     ${RESP}     key=name
    should not be empty     ${name}


TR-20192: update valid cloud control group
    [Documentation]         update valid cloud control group for one/multiple devices IDs
    [Tags]                  tcxm_20192   development
    Depends On              tcxm_20185
    ${RESP} =               xapi Update Cloud Control Group     ${CCG_ID}    {"name": "upd-valid-ccg-ssid1", "description": "update valid cloud config group for ssid1", "device_ids": [${DEVICE_ID}]}
    ${name} =               get json values     ${RESP}     key=name
    ${description} =        get json values     ${RESP}     key=description
    ${device_ids} =         get json values     ${RESP}     key=device_ids
    should be equal as strings      '${name}'             'upd-valid-ccg-ssid1'
    should be equal as strings      '${description}'      'update valid cloud config group for ssid1'
    should not be empty     ${device_ids}

TR-20193: update partial invalid cloud control group
    [Documentation]         update partial invalid cloud control group for one bad device ID
    [Tags]                  tcxm_20193   development
    Depends On              tcxm_20185
    ${RESP} =               xapi Update Cloud Control Group     ${CCG_ID}    {"name": "upd-partial-valid-ccg-ssid1", "description": "update partial invalid cloud control group for ssid1", "device_ids": [${DEVICE_ID}, 0]}
    ${RESP_CODE} =          Get Response Code   ${RESP}
    should be equal as strings          '${RESP_CODE}'     '${INVALID_ARGUMENT}'

TR-20194: update invalid cloud control group
    [Documentation]         update invalid cloud control group for one bad device ID
    [Tags]                  tcxm_20194   development
    Depends On              tcxm_20185
    ${RESP} =               xapi Update Cloud Control Group     ${CCG_ID}    {"name": "upd-invalid-ccg-ssid1", "description": "update invalid cloud control group for ssid1", "device_ids": [0]}
    ${RESP_CODE} =          Get Response Code   ${RESP}
    should be equal as strings          '${RESP_CODE}'     '${INVALID_ARGUMENT}'

    [Teardown]
    ${RESP_CODE} =          xapi Delete Cloud Control Group    ${CCG_ID}
    should be true          ${RESP_CODE}==1